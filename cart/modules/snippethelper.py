from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
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


def has_variant_column():
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


def scart_data_setup(cart, lst=[]):
    for key in cart:
        quantity = int(cart[key]['quantity'])

        if key.startswith('v-'):
            variant = ProductVariant.objects.get(id=int(key.split('-', 1)[1]))
            price = variant.sale_price if variant.sale_price else variant.price
            image = variant.images.filter(thumbnail=True).first() or variant.images.first()
            name = variant.title
            product_id = variant.product.id
        else:
            product = Product.objects.get(id=int(key.split('-', 1)[1]) if '-' in key else int(key))
            price = product.price
            image = product.images.filter(thumbnail=True).first() if product.images.filter(thumbnail=True).exists() else None
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
        for i in cart:
            if i.startswith('v-'):
                variant = ProductVariant.objects.get(id=int(i.split('-', 1)[1]))
                price = variant.sale_price if variant.sale_price else variant.price
                calc_cart(int(cart[i]['quantity']), price)
            else:
                product = Product.objects.get(id=int(i.split('-', 1)[1]) if '-' in i else int(i))
                calc_cart(int(cart[i]['quantity']), product.price)
        return items, total

    for i in cart:
        price = i.variant.sale_price if i.variant and i.variant.sale_price else (i.variant.price if i.variant else i.product.price)
        calc_cart(i.quantity, price)

    return items, total
