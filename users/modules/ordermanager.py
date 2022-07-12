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
            
            # record instance
            # create a new instance deliver address data
            delivery = Delivery_Address_Details.objects.create(name=name, last_name=lastname, city_town=city, street_name=street, building_appartment=building, phone_number=phone, delivery_details=information, user=user, default=state)

        else:
            # return form as it is to reload it 
            return (False, form)
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
    # current cart total Note the cart context process returns a list 
    # of two values at index 0 the item in cart total quantity and at index 1 the 
    # cart total amount in usd
    total = "{:.2f}".format(managecart.cart_context_process()[1])
    # is instance 
    # create an new order object model
    order = Orders.objects.create(user=user, address=delivery, total=total, note=note)


    # loop over current user cart 
    # Add each item in the place order cart to the order items objects
    # and remove each added item from cart 
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
    
    return (True, order)

# dict -> dict * boolean
# takes request dict return: form data
# and boolean true if user have address saved or false if not
def address_post(request):
    # is instance form
    # new delivery address for login user
    form =request.POST
    try:
        form['current_address_id']
        # new address 
        state = False

    except:
        # is dict                                                  
        # conatin current select address id and order note
        form = Delivery_Information(request.POST)
        # is a helper function at modules, ordermanager 
        # user have saved address
        state = True 

    return form, state
            