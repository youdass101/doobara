from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from functools import lru_cache
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
