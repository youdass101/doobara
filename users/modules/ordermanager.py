from ..models import *
from ..forms import *
from cart.modules.cartmanager import *
from cart.modules.snippethelper import *


def createorder(request, form, new):
    user = request.user
    # result = create_new_address(request, form)
    if new:
        if form.is_valid():
        # if result:
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
            note = form.cleaned_data.get('notes')
            form.instance.user = user
            form.instance.default = state
            delivery =form.save()        

        else:
            # return form as it is to reload it 
            return (False, form)
    else:
        # is instance object
        # current saved in data address
        id = int(form['current_address_id'])
        note = form['ordernote']
        delivery = Delivery_Address_Details.objects.get(id=id)
        
    # is instance | (loc: cart.modules.cartmanager)
    # cart manager class instance to add remove and update cart 
    managecart = CartManager(request)
    # is float 
    # current cart total Note the cart context process returns a list 
    # of two values at index 0 the item in cart total quantity and at index 1 the 
    # cart total amount in usd
    # total = "{:.2f}".format(managecart.cart_context_process()[1])
    total = "{:.2f}".format(cart_context_process(request)[1])

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
def address_post(form):
    # aleardy existing address (icluding any order note in form)
    try:
        form['current_address_id']
        # user have saved address
        state = False
        
    # new delivery address for logged in user (should include order note)
    except:
        # is dict                                              
        form = Delivery_Information(form)
        # is a helper function at modules, ordermanager 
        # new address 
        state = True 

    return form, state
            
def change_default_address(user, aid):
    # get current default addres and set it to default to false and and save model instance
    # loc: models
    old = Delivery_Address_Details.objects.get(user=user, default=True)
    old.default = False
    old.save()
    # set new address to default 
    # get new address and set default to true and save instance
    caddress = Delivery_Address_Details.objects.get(id=aid)
    caddress.default = True
    caddress.save()


def create_new_address(request, form):
    if form.is_valid:
        # add missing fields to form and save form to instance 
        form.instance.user = request.user
        form.instance.default = False
        form.save()
        return True
    else:
        return form

