from decimal import Decimal

from django.db.models import Q
from django.utils import timezone

from cart.models import Cart_Item
from shop.models import Product, ProductVariant, NormalProductVariant

from .models import Coupon, CouponUsage

SESSION_COUPON_CODE_KEY = "applied_coupon_code"
SESSION_COUPON_FEEDBACK_KEY = "applied_coupon_feedback"


def normalize_coupon_code(code):
    """Normalize human-entered coupon codes so lookups are deterministic."""
    return (code or "").strip().upper()


def store_coupon_in_session(request, code):
    """Persist one coupon code in session; this enforces single-coupon usage."""
    request.session[SESSION_COUPON_CODE_KEY] = normalize_coupon_code(code)
    request.session.save()


def remove_coupon_from_session(request):
    """Remove the applied coupon from session when user explicitly clears it."""
    if SESSION_COUPON_CODE_KEY in request.session:
        del request.session[SESSION_COUPON_CODE_KEY]
        request.session.save()


def set_coupon_feedback(request, message, level):
    """Store one short coupon feedback message to show after redirect."""
    request.session[SESSION_COUPON_FEEDBACK_KEY] = {"message": message, "level": level}
    request.session.save()


def pop_coupon_feedback(request):
    """Read and clear one-time feedback so coupon UI can show actionable errors."""
    feedback = request.session.pop(SESSION_COUPON_FEEDBACK_KEY, None)
    request.session.save()
    return feedback


def get_session_coupon_code(request):
    """Return normalized code currently stored in session, if any."""
    return normalize_coupon_code(request.session.get(SESSION_COUPON_CODE_KEY, ""))


def find_active_coupon_by_code(code, at_time=None):
    """Find active coupon by code and date-window constraints."""
    normalized = normalize_coupon_code(code)
    if not normalized:
        return None

    now = at_time or timezone.now()
    return (
        Coupon.objects.filter(code__iexact=normalized, active=True)
        .filter(Q(valid_from__isnull=True) | Q(valid_from__lte=now))
        .filter(Q(valid_until__isnull=True) | Q(valid_until__gte=now))
        .prefetch_related("products", "categories")
        .first()
    )


def _build_cart_lines(request):
    """Build lightweight cart-line data used by validation and discount calculations."""
    lines = []
    if request.user.is_authenticated:
        cart_items = Cart_Item.objects.filter(cart__user=request.user).select_related(
            "product", "variant", "normal_variant"
        )
        for item in cart_items:
            price = item.product.sale_price if item.product.sale_price else item.product.price
            if item.variant:
                price = item.variant.sale_price if item.variant.sale_price else item.variant.price
            elif item.normal_variant:
                price = item.normal_variant.sale_price if item.normal_variant.sale_price else item.normal_variant.price
            lines.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "line_subtotal": Decimal(str(price)) * item.quantity,
                }
            )
        return lines

    session_cart = request.session.get("cart", {})
    if not isinstance(session_cart, dict) or not session_cart:
        return lines

    product_ids, variant_ids, normal_variant_ids = set(), set(), set()
    for key in session_cart.keys():
        if key.startswith("sv-") or key.startswith("v-"):
            variant_ids.add(int(key.split("-", 1)[1]))
        elif key.startswith("nv-"):
            normal_variant_ids.add(int(key.split("-", 1)[1]))
        elif key.startswith("p-"):
            product_ids.add(int(key.split("-", 1)[1]))
        else:
            product_ids.add(int(key))

    product_map = {p.id: p for p in Product.objects.filter(id__in=product_ids)}
    variant_map = {v.id: v for v in ProductVariant.objects.filter(id__in=variant_ids)}
    normal_variant_map = {nv.id: nv for nv in NormalProductVariant.objects.filter(id__in=normal_variant_ids)}

    for key, data in session_cart.items():
        quantity = int(data.get("quantity", 0) or 0)
        if quantity <= 0:
            continue
        if key.startswith("sv-") or key.startswith("v-"):
            variant = variant_map.get(int(key.split("-", 1)[1]))
            if not variant:
                continue
            price = variant.sale_price if variant.sale_price else variant.price
            product_id = variant.product_id
        elif key.startswith("nv-"):
            normal_variant = normal_variant_map.get(int(key.split("-", 1)[1]))
            if not normal_variant:
                continue
            price = normal_variant.sale_price if normal_variant.sale_price else normal_variant.price
            product_id = normal_variant.product_id
        elif key.startswith("p-"):
            product = product_map.get(int(key.split("-", 1)[1]))
            if not product:
                continue
            price = product.sale_price if product.sale_price else product.price
            product_id = product.id
        else:
            product = product_map.get(int(key))
            if not product:
                continue
            price = product.sale_price if product.sale_price else product.price
            product_id = product.id

        lines.append(
            {
                "product_id": product_id,
                "quantity": quantity,
                "line_subtotal": Decimal(str(price)) * quantity,
            }
        )
    return lines


def check_subtotal_threshold(coupon, subtotal):
    """Check coupon minimum subtotal guard against current cart subtotal."""
    subtotal_decimal = Decimal(str(subtotal))
    if subtotal_decimal < coupon.minimum_subtotal:
        return False, f"Coupon requires a minimum subtotal of ${coupon.minimum_subtotal:.2f}."
    return True, ""


def check_usage_limits(coupon, user):
    """Check global and per-user usage limits using successful usage records only."""
    total_count = CouponUsage.objects.filter(coupon=coupon).count()
    if coupon.usage_limit_total is not None and total_count >= coupon.usage_limit_total:
        return False, "This coupon has reached its total usage limit."

    if user and user.is_authenticated and coupon.usage_limit_per_user is not None:
        user_count = CouponUsage.objects.filter(coupon=coupon, user=user).count()
        if user_count >= coupon.usage_limit_per_user:
            return False, "You already used this coupon the maximum number of times."

    return True, ""


def check_coupon_applicability_to_cart(coupon, cart_lines):
    """Return line-subtotal eligible for discount, based on product/category targeting rules."""
    if coupon.applies_to_all:
        eligible_subtotal = sum((line["line_subtotal"] for line in cart_lines), Decimal("0.00"))
        return eligible_subtotal, True

    product_ids = {line["product_id"] for line in cart_lines if line.get("product_id")}
    if not product_ids:
        return Decimal("0.00"), False

    eligible_product_ids = set(coupon.products.filter(id__in=product_ids).values_list("id", flat=True))

    if coupon.categories.exists():
        category_product_ids = set(
            coupon.categories.filter(products__id__in=product_ids).values_list("products__id", flat=True)
        )
        eligible_product_ids.update(category_product_ids)

    eligible_subtotal = Decimal("0.00")
    for line in cart_lines:
        if line.get("product_id") in eligible_product_ids:
            eligible_subtotal += line["line_subtotal"]

    return eligible_subtotal, eligible_subtotal > 0


def calculate_discount_amount(coupon, eligible_subtotal):
    """Calculate discount amount and clamp to eligible subtotal to avoid negatives."""
    eligible_subtotal = Decimal(str(eligible_subtotal))
    if eligible_subtotal <= 0:
        return Decimal("0.00")

    if coupon.discount_type == Coupon.DISCOUNT_PERCENT:
        discount = (eligible_subtotal * coupon.value) / Decimal("100")
    else:
        discount = coupon.value

    if discount < 0:
        discount = Decimal("0.00")
    if discount > eligible_subtotal:
        discount = eligible_subtotal

    return discount.quantize(Decimal("0.01"))


def validate_coupon_for_request(request, subtotal, at_time=None):
    """Validate currently applied coupon against cart, date, subtotal, and usage rules."""
    code = get_session_coupon_code(request)
    result = {
        "ok": False,
        "code": code,
        "coupon": None,
        "discount_amount": Decimal("0.00"),
        "eligible_subtotal": Decimal("0.00"),
        "error": "",
    }

    if not code:
        return result

    coupon = find_active_coupon_by_code(code, at_time=at_time)
    if not coupon:
        result["error"] = "Coupon is invalid or expired."
        return result

    cart_lines = _build_cart_lines(request)
    if not cart_lines:
        result["error"] = "Coupons cannot be applied to an empty cart."
        return result

    subtotal_ok, subtotal_error = check_subtotal_threshold(coupon, subtotal)
    if not subtotal_ok:
        result["error"] = subtotal_error
        return result

    usage_ok, usage_error = check_usage_limits(coupon, request.user)
    if not usage_ok:
        result["error"] = usage_error
        return result

    eligible_subtotal, applicable = check_coupon_applicability_to_cart(coupon, cart_lines)
    if not applicable:
        result["error"] = "Coupon does not apply to products currently in your cart."
        return result

    discount_amount = calculate_discount_amount(coupon, eligible_subtotal)
    if discount_amount <= 0:
        result["error"] = "Coupon does not reduce the current cart total."
        return result

    result.update(
        {
            "ok": True,
            "coupon": coupon,
            "discount_amount": discount_amount,
            "eligible_subtotal": eligible_subtotal,
            "error": "",
        }
    )
    return result


def get_coupon_pricing_for_request(request, subtotal):
    """Return coupon pricing payload for cart/checkout totals and UI display."""
    validation = validate_coupon_for_request(request, subtotal)
    return {
        "coupon_code": validation["code"],
        "coupon": validation["coupon"],
        "coupon_valid": validation["ok"],
        "coupon_discount": validation["discount_amount"] if validation["ok"] else Decimal("0.00"),
        "coupon_error": validation["error"] if not validation["ok"] and validation["code"] else "",
    }


def snapshot_coupon_to_order(order, pricing):
    """Copy coupon details to order so history does not depend on mutable coupon records."""
    order.coupon_code = pricing.get("coupon_code", "") or ""
    order.coupon_discount_amount = pricing.get("coupon_discount", Decimal("0.00"))
    order.save(update_fields=["coupon_code", "coupon_discount_amount"])


def record_coupon_usage(order, pricing):
    """Record usage only after order success, so abandoned checkouts do not consume limits."""
    coupon = pricing.get("coupon")
    discount = pricing.get("coupon_discount", Decimal("0.00"))
    if not coupon or discount <= 0:
        return None

    return CouponUsage.objects.create(
        coupon=coupon,
        user=order.user if order.user.is_authenticated else None,
        order=order,
        coupon_code_snapshot=pricing.get("coupon_code", coupon.code),
        discount_amount=discount,
    )
