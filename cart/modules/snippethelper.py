from shop.models import *
from ..models import *

# This a helper mini functions for cart application 

# NOTES FOR OPTIMIZATION 
# scart_data_setup function can be replace with the session cart itself 
# but the session cart pattern should be costumized to match the cds function output pattern


# instance -> boolean
# check if given dict is empty 
def cart_empty(cart):
    if len(cart)== 0:
        return True
    else:
        return False

# list(object) -> integer
# take list of address and return ID of the one that have default as true 
def default_address(lod):
    for i in lod:
        if i['default']:
            return int(i['id'])
    return 0


# list_of_instace -> list_of_dict
# create a default dict template of user cart data for session
# mimicing model serialization pattern
def scart_data_setup(cart, lst=[]):
    for i in cart:
        # is object model 
        # product object with given id 
        product = Product.objects.get(id=i)
        # convert product data to dict with required keys and append dict to list
        #  serialization
        lst.append(({"productname" : product.name,
                "productid" : product.id,
                "productunitprice" : product.price,
                "productquantity": cart[i]['quantity'],
                "productimage": product.album.default().serialize()}, 
                (int(cart[i]['quantity']) * float(product.price))
                ))

    return lst



# dict -> object * object
# helper that take request and return user or session data (user object or session dict
# and user cart or session cart) depend if user logged in
def userorsession(request):
    # if user logged in
    if request.user.is_authenticated:
        # is model object (class local)
        # logged in user object
        user = request.user
        # check if user have my cart linked
        try:
            # is model object (class local)
            # logged in user in cart items
            cart = user.mycart.items.all()

        # create new cart and linke it 
        except:
            # is model object (class local)
            # empty cart linked created 
            cart = [Cart.objects.create(user=user)]

    # User not loged in   
    # use the session insted of user
    else:
        # is dict (class local)
        # user session dict
        user = request.session
        # if cart key exist
        try:
            # is dict
            cart = user['cart']
        # create a new cart key
        except:
            # empty cart 
            user['cart'] = {}
            # sace to session
            user.save()
            # is dict
            cart = user.get('cart')
    
    return user, cart
    
def cart_context_process(request):
        # is int 
        # the all page cart update data for top and other use
        items, total = 0, 0
        # is dict
        user, cart = userorsession(request)
        # int * int -> true
        # calculate the cart qtt and total price
        def calc_cart (qtt, price):
            nonlocal items, total
            items += qtt
            total += (float(qtt)*float(price))

        # loop over user cart item and can calculate totalt and item in cart qtt 
        for i in cart:
            # if user is logged in
            if request.user.is_authenticated:
                calc_cart(i.quantity, i.product.price)
            # if user is not logged in 
            else:
                # is instance 
                # to keep price updated in cart we called the prduct price
                product = Product.objects.get(id = i)
                # calling the inner helper to get the totale and items qtt
                calc_cart(int(cart[i]['quantity']), product.price)

        
        return items, total