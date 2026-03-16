from ..models import *
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
# project files
from .snippethelper import *


@receiver(user_logged_in)
def cart_after_login(request, **kwargs):
    userorsession(request)
    cart_migration(request)


def cart_migration(request):
    if not has_variant_column():
        return

    user_cart = request.user.mycart.items.all()
    session_cart = ensure_session_cart(request.session)

    if cart_empty(user_cart) and (not cart_empty(session_cart)):
        for key in session_cart:
            itemdetail = {'pid': key, 'quantity': session_cart[key]['quantity']}
            cart = CartManager(request)
            cart.add_to_cart(itemdetail)


class CartManager:
    def __init__(self, request):
        self.request = request
        self.user, self.cart = userorsession(request)
        self.uli = request.user.is_authenticated and not isinstance(self.cart, dict)

    def cart_page(self):
        if self.uli:
            ccart = []
            for item in self.cart:
                unit_price = item.variant.sale_price if item.variant and item.variant.sale_price else (item.variant.price if item.variant else item.product.price)
                ccart.append((item.serialize(), (item.quantity * unit_price)))
        else:
            ccart = scart_data_setup(self.cart, [])
        return ccart

    def _parse_item_identifier(self, item):
        variant_id = item.get('variant_id')
        pid = item.get('pid')

        if variant_id:
            return ('variant', int(variant_id))

        if not pid:
            raise ValueError('Missing cart identifier')

        if isinstance(pid, str) and '-' in pid:
            kind, raw_id = pid.split('-', 1)
            if kind == 'v':
                return ('variant', int(raw_id))
            return ('product', int(raw_id))

        return ('product', int(pid))

    def add_to_cart(self, item):
        item_type, item_id = self._parse_item_identifier(item)
        pqtt = int(item['quantity'])

        if item_type == 'variant':
            variant = ProductVariant.objects.get(id=item_id)
            product = variant.product
            cart_key = f'v-{variant.id}'
        else:
            product = Product.objects.get(id=item_id)
            variant = None
            cart_key = f'p-{product.id}'

        if self.uli:
            try:
                if variant:
                    citem = Cart_Item.objects.get(variant=variant, cart=self.user.mycart)
                else:
                    citem = Cart_Item.objects.get(product=product, variant__isnull=True, cart=self.user.mycart)
                citem.quantity += pqtt
                citem.save()
                if citem.quantity == 0:
                    citem.delete()
            except:
                Cart_Item.objects.create(product=product, variant=variant, quantity=pqtt, cart=self.user.mycart)

        else:
            try:
                qtt = int(self.user['cart'][cart_key]['quantity'])
                self.user['cart'][cart_key]['quantity'] = str(qtt + pqtt)
                if (qtt + pqtt) == 0:
                    del self.user['cart'][cart_key]
            except:
                self.user['cart'][cart_key] = {'quantity': str(pqtt)}

            self.user.save()

        return True

    def update_cart(self, cupdate):
        try:
            self.add_to_cart(cupdate['cart'])
        except:
            if self.uli:
                cart = self.cart
                current_quantities = {item.serialize()['cartkey']: item.quantity for item in cart}
            else:
                cart = self.cart.copy()
                current_quantities = {key: int(cart[key]['quantity']) for key in cart}

            for product in cupdate['cart']:
                cart_key = product['pid']
                given = int(product['quantity'])
                current = current_quantities.get(cart_key, 0)
                result = {'pid': cart_key, 'quantity': (given - current)}
                self.add_to_cart(result)
        return True

    def delete_objct(self, item, ucart):
        Cart_Item.objects.get(product=item, cart=ucart).delete()
        return True
