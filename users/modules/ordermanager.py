from ..models import *
from ..forms import *
from cart.modules.cartmanager import *

def createorder(request, form, new):
    user = request.user
    if new:
        if form.is_valid():
            # clean form data of delivery address form 
            name = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city_town']
            street = form.cleaned_data['street']
            building = form.cleaned_data['building_appartement']
            information = form.cleaned_data['additional_information']
            note = form.cleaned_data['note']

            # is intance 
            # create a new delivery address model object 
            state = False
            # is list
            # list of user saved delivery addresses
            allad = user.myaddress.all()
           
            if len(allad) == 0:
                state=True
            delivery = Delivery_Address_Details.objects.create(name=name, last_name=lastname, city_town=city, street_name=street, building_appartment=building, phone_number=phone, delivery_details=information, user=user, default=state)
        else:
            return False
    else:
        # is instance object
        # current saved in data address
        id = int(form['current_address_id'])
        note = form['ordernote']
        delivery = Delivery_Address_Details.objects.get(id=id)
    # is instance 
    # cart manager class instance to add remove and update cart 
    managecart = CartManager(request)
    # is float 
    # current cart totla 
    total = "{:.2f}".format(managecart.cart_context_process()[1])
    # is instance 
    # create an new order object model
    order = Orders.objects.create(user=user, address=delivery, total=total, note=note)


    # loop over current user cart 
    for item in user.mycart.items.all():
        # create new item order model object
        Item_Order.objects.create(product=item.product, quantity=item.quantity, price=item.product.price, product_name=item.product.name, order=order)
        # is instance
        # product model instance 
        product = item.product
        # is instance 
        # current user cart model instance 
        cart = user.mycart
        # delete current product from current user cart
        managecart.delete_objct(product, cart)
    
    return order
 


            