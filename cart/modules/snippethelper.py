from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from functools import lru_cache
from decimal import Decimal
from shop.models import *
from ..models import *


# This a helper mini functions for cart application

def cart_empty(cart):
    if len(cart)== 0:
        return True
    else:
        return False


def default_address(lod):
    for i in lod:
        if i['default']:
            return int(i['id'])
    return 0


@lru_cache(maxsize=1)
def has_variant_column():
    # PERF: schema introspection is expensive; cache this for process lifetime.
    # If schema changes at runtime, restarting app workers will refresh this value.
    try:
        with connection.cursor() as cursor:
            columns = connection.introspection.get_table_description(cursor, Cart_Item._meta.db_table)
        return any(column.name == 'variant_id' for column in columns)
    except Exception:
        return False


def ensure_session_cart(session):
    if 'cart' not in session:
        session['cart'] = {}
        session.save()
    return session['cart']


def _parse_cart_key(key):
    # Normalized parser for both legacy keys ("12") and typed keys ("p-12"/"v-7")
    if key.startswith('v-'):
        return ("variant", int(key.split('-', 1)[1]))
    if key.startswith('p-'):
        return ("product", int(key.split('-', 1)[1]))
    return ("product", int(key))


def _load_session_cart_maps(cart):
    # PERF: bulk-load Product/ProductVariant rows once instead of querying in each loop iteration.
    product_ids, variant_ids = set(), set()
    for key in cart.keys():
        kind, object_id = _parse_cart_key(key)
        if kind == "variant":
            variant_ids.add(object_id)
        else:
            product_ids.add(object_id)

    products = Product.objects.filter(id__in=product_ids).prefetch_related("images")
    variants = ProductVariant.objects.filter(id__in=variant_ids).select_related("product").prefetch_related("images")
    return {p.id: p for p in products}, {v.id: v for v in variants}


def scart_data_setup(cart, lst=None):
    # Avoid mutable default argument so results never leak across calls.
    if lst is None:
        lst = []

    # PERF: load all referenced products/variants up-front and reuse in-memory maps.
    product_map, variant_map = _load_session_cart_maps(cart)

    for key in cart:
        quantity = int(cart[key]['quantity'])

        kind, object_id = _parse_cart_key(key)
        if kind == "variant":
            variant = variant_map.get(object_id)
            if not variant:
                continue
            price = variant.sale_price if variant.sale_price else variant.price
            image = variant.images.filter(thumbnail=True).first() or variant.images.first()
            name = variant.title
            product_id = variant.product.id
        else:
            product = product_map.get(object_id)
            if not product:
                continue
            price = product.price
            # PERF: one query path instead of .exists()+.first() double query.
            image = product.images.filter(thumbnail=True).first() or product.images.first()
            name = product.name
            product_id = product.id

        lst.append(({
            "productname": name,
            "productid": product_id,
            "productunitprice": price,
            "productquantity": quantity,
            "productimage": image,
            "cartkey": key,
        }, (quantity * float(price))))

    return lst


def userorsession(request):
    if request.user.is_authenticated:
        if not has_variant_column():
            return request.session, ensure_session_cart(request.session)

        user = request.user
        try:
            cart = user.mycart.items.all()
        except (ProgrammingError, OperationalError):
            return request.session, ensure_session_cart(request.session)
        except:
            cart = [Cart.objects.create(user=user)]
    else:
        user = request.session
        cart = ensure_session_cart(user)

    return user, cart


def cart_context_process(request):
    items, total = 0, 0
    user, cart = userorsession(request)

    def calc_cart(qtt, price):
        nonlocal items, total
        items += qtt
        total += (float(qtt)*float(price))

    if isinstance(cart, dict):
        # PERF: use bulk-loaded maps to avoid one DB query per cart key.
        product_map, variant_map = _load_session_cart_maps(cart)
        for i in cart:
            kind, object_id = _parse_cart_key(i)
            if kind == "variant":
                variant = variant_map.get(object_id)
                if not variant:
                    continue
                price = variant.sale_price if variant.sale_price else variant.price
                calc_cart(int(cart[i]['quantity']), price)
            else:
                product = product_map.get(object_id)
                if not product:
                    continue
                calc_cart(int(cart[i]['quantity']), product.price)
        return items, total

    for i in cart:
        price = i.variant.sale_price if i.variant and i.variant.sale_price else (i.variant.price if i.variant else i.product.price)
        calc_cart(i.quantity, price)

    return items, total


def get_active_shipping_methods():
    """
    Return active shipping methods ordered for display in cart/checkout selectors.
    """
    return Shipping_Method.objects.filter(active=True).order_by("sort_order", "id")


def get_selected_shipping_method(request):
    """
    Resolve the selected shipping method for authenticated/session carts.
    Falls back to the first active method when no explicit selection exists.
    """
    methods = list(get_active_shipping_methods())
    if not methods:
        return None

    default_method = methods[0]
    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user).select_related("shipping_method").first()
        if cart_obj and cart_obj.shipping_method and cart_obj.shipping_method.active:
            return cart_obj.shipping_method
        return default_method

    session_method_id = request.session.get("shipping_method_id")
    if session_method_id:
        for method in methods:
            if method.id == int(session_method_id):
                return method
    return default_method


def set_selected_shipping_method(request, method_id):
    """
    Persist selected shipping method on cart/session, validating active method IDs.
    """
    method = Shipping_Method.objects.filter(id=method_id, active=True).first()
    if not method:
        return None

    if request.user.is_authenticated:
        cart_obj = Cart.objects.filter(user=request.user).first()
        if cart_obj:
            cart_obj.shipping_method = method
            cart_obj.save(update_fields=["shipping_method"])
    else:
        request.session["shipping_method_id"] = method.id
        request.session.save()

    return method


def cart_pricing_breakdown(request):
    """
    Centralized cart pricing:
    - subtotal comes from cart items
    - shipping cost comes from selected shipping method
    - total is subtotal + shipping
    """
    _, subtotal = cart_context_process(request)
    shipping_method = get_selected_shipping_method(request)
    shipping_price = Decimal(str(shipping_method.price if shipping_method else 0))
    subtotal_decimal = Decimal(str(subtotal))
    total = subtotal_decimal + shipping_price
    return {
        "subtotal": subtotal_decimal,
        "shipping_price": shipping_price,
        "total": total,
        "shipping_method": shipping_method,
    }
