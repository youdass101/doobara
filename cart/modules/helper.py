# from os import scandir
# from pickle import TRUE
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


# dict -> boolean
# delete object using product given id 
# Helper function to delete object in a pattern 
def del_object(item, ucart):
    # is model object instance exist
    product= Product.objects.get(id=item)
    # delete object
    Cart_Item.objects.get(product= product, cart=ucart).delete()


def update_cart(request, cartupdate):
    if request.user.is_authenticated:
        # is dict of objects
        user_cart = request.user.mycart
        # if delete value is true when x button is pressed in cart
        try: 
            del_object(cartupdate['cart']['pid'], user_cart)
           
        except:
            # loop over products in cart html
            for product in cartupdate['cart']:
                # is model instance 
                # single product object 
                po = Product.objects.get(id = int(product['pid']))
                # is model instance
                # Cart item in cart items related to use user 
                cit = Cart_Item.objects.get(product= po, cart=user_cart)
                # if new giver quatity is 0 delete product from cart item
                if (int(product['quantity']) == 0):
                    cit.delete()
                else:
                    # if new given qunatity is more than 0, adjust it
                    cit.quantity = int(product['quantity'])
                    cit.save()

    else:
        # is dict
        # the current session cart in request class 
        cart = request.session['cart']
        try:
            # delete the prouct from cart id the update given is for single product not list
            del cart[cartupdate['cart']['pid']]  
        except:
            # loop over list of product dict in cart html session
            for product in cartupdate['cart']:  
                # if new product quantity is 0 delete product from session cart
                if (int(product['quantity']) == 0 ):
                    del cart[product['pid']]
                else:
                    # if new given quantity is more than 0 change the current session 
                    # quantity to the given quantity
                    cart[product['pid']]['quantity'] = product['quantity']
        request.session.save()

def cart_context_process(request):
    # is int 
    # the all page cart update data for top and other use
    items, total = 0, 0
    # int * int -> true
    # calculate the cart qtt and total price
    def calc_cart (qtt, price):
        nonlocal items, total
        items += qtt
        total += (float(qtt)*float(price))
    # if user is logged in
    if request.user.is_authenticated:
        user = request.user
        try:
            # is listofproduct
            cart = user.mycart.items.all()
            for i in cart:
                # update items qtt and total price of user cart
                calc_cart(i.quantity, i.product.price)   
        except:
            # is dict
            cart = [Cart.objects.create(user=user)]  
    # if user is not logged in
    else:      
        try:
            cart = request.session['cart']
            for i in cart:
                # update items qtt and total pruce of session cart
                calc_cart(int(cart[i]['quantity']), cart[i]['price'])
        except:
            # is dict
            # create a new cart session 
            request.session['cart'] = {}
            request.session.save()
    return items, total

# def ccs(request):
#     try:
#         dcart = request.session['cartclass']
#     except:
#         request.session['cartclass'] = CartManager(request)
#         dcart = request.session['cartclass']
#     return dcart

class CartManager:
    def __init__(self, request):
        self.request = request
        try:
            self.user = self.request.user
            try:
                self.cart = self.user.mycart.items.all()
            except:
                self.cart = [Cart.objects.create(user=self.user)]
        except:
            self.user = self.request.session
            try:
                self.cart = self.user['cart']
            except:
                self.user['cart'] = {}
                self.user.save()
                self.cart = self.user['cart']