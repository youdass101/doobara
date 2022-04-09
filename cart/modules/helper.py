from os import scandir
from ..models import *

# dict * dict -> boolean (event)
# add item in "item" to loggedin user "in request" cart "in models"
# if user cart object exist add item else create table object
# if item exist in cart adjust value else create item object  
def user_add_to_cart (request, item, product):
    
    # is object
    # load current loggedin user object model 
    user = request.user

    # is int
    # quantity keyvalue in given item dict
    iqtt = int(item['quantity'])

    # object * string * object -> boolean
    # create object using the fgiven data
    def create_ci (product, qtt, cart):
        Cart_Item.objects.create(product=product, quantity=qtt, cart=cart)

    try:
        # if use have object cart
        mycart = user.mycart
        # manupilating object data to update to the new given data
        # If product item object already exist adjust
        try:
            # is object 
            # single object from cart item model 
            citem = Cart_Item.objects.get(product=product, cart=mycart)
            # is int 
            # updating incrementing sub value by given int item 
            citem.quantity += iqtt
            citem.save()
        # if previous failed excute this supose element does'nt exist
        except:
            # if product item doesn't exist create new
            create_ci(product, iqtt, mycart)
    except:
        # If user cart object doesn't exist create new one
        Cart.objects.create(user=user)
        create_ci(product, iqtt, user.mycart)

    return True

# dict * dict -> dict
# if session doesn't exist create new one 
# save or adjust cart data in session dict with given item
def session_add_to_cart (request, item, product):

    # is int
    # extract int price from given object product  
    price = product.price
    # is hex
    # extract int session dict from request class 
    session = request.session
    # is int
    # quantity keyvalue in given item dict
    iqtt = int(item['quantity'])

    # add and edit data in session dict
    try:
        qtt = int(session['cart'][item['pid']]['quantity'])
        session['cart'][item['pid']]['quantity'] = str(qtt + iqtt)
    except:
        session['cart'][item['pid']] = {'quantity' : str(iqtt), 'price' : str(price)}
    
    request.session.save()

# dict -> list of dict
# take the session cart dict and return a list of dict for prodduct 
def session_cart(cart):
    # is list 
    # empty session cart to be filled 
    scart = []
    for i in cart:
            product = Product.objects.get(id=i)
            scart.append(({"productname" : product.name,
                    "productid" : product.id,
                    "productunitprice" : cart[i]['price'],
                    "productquantity": cart[i]['quantity'],
                    "productimage": product.album.default().serialize()}, 
                    (int(cart[i]['quantity']) * float(cart[i]['price']))
                    ))
    return scart
