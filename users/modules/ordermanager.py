from ..models import *
from ..forms import *
from cart.modules.cartmanager import *

def createorder(request, form):
    user = request.user
    if form.is_valid():
        name = form.cleaned_data['first_name']
        lastname = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        city = form.cleaned_data['city_town']
        street = form.cleaned_data['street']
        building = form.cleaned_data['building_appartement']
        information = form.cleaned_data['additional_information']
        note = form.cleaned_data['note']
        delivery = Delivery_Address_Details.objects.create(name=name, last_name=lastname, city_town=city, street_name=street, building_appartment=building, phone_number=phone, delivery_details=information, user=user)
        managecart = CartManager(request)
        total = "{:.2f}".format(managecart.cart_context_process()[1])
        order = Orders.objects.create(user=user, address=delivery, total=total, note="")

        for item in user.mycart.items.all():
            od = Item_Order.objects.create(product=item.product, quantity=item.quantity, price=item.product.price, product_name=item.product.name, order=order)
            pr = item.product
            ct = user.mycart
            managecart.delete_objct(pr, ct)

            