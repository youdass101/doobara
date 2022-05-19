# from os import scandir
# from pickle import TRUE
from ..models import *
from allauth.account.signals import user_logged_in
from django.dispatch import receiver

# When user login 
@receiver(user_logged_in)
def cart_after_login(request, **kwargs):
    cart_migration(request)

# dict -> boolean 
# move session cart item to use cart data if user cart is empty
def cart_migration(request):
    user_cart = request.user.mycart.items.all()
    session_cart = request.session['cart']
    if user_cart_empty(user_cart) and session_cart_not_empty(session_cart):
        for item in session_cart:
            itemdetail = {'pid': item, 'quantity': session_cart[item]['quantity']}
            cart = CartManager(request)
            cart.add_to_cart(itemdetail)

# dict -> boolean
# check if given dict is empty
def session_cart_not_empty(cart):
    if len(cart)== 0:
        return False
    else:
        return True

# instance -> boolean
# check if given dict is empty 
def user_cart_empty(cart):
    if len(cart)== 0:
        return True
    else:
        return False



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
            cart = [Cart.objects.create(user=user)].items.all()
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


# Object 
# Manage all cart request add, update, view and delete
class CartManager:
    # object * dict -> *
    # object initial and default variables
    def __init__(self, request):
        # is dict
        # django request dict
        self.request = request
        # is obejct or dict
        # user object or session dict and user cart object or session cart dict 
        self.user, self.cart = userorsession(request)
        # is boolean
        # true is user is logged in, else false
        self.uli = request.user.is_authenticated
    
    # object -> listofdict 
    # if user is auth it will serialize self.cart using model serializer
    # if no user is logged it will create a listofdict from session cart dict data 
    # same listofdict template for both options
    def cart_page(self):
        # if self cart is a model object
        if self.uli:
            # is listofdict 
            # serialized cart objects in self.cart
            ccart = [(item.serialize(),(item.quantity * item.product.price)) for item in self.cart]
        # if self cart is session dict
        else:
            # is list
            # empty list pre assinged to be used in loop
            ccart = []
            # for key in list of dict cart
            for i in self.cart:
                    # is object model 
                    # product object with given id 
                    product = Product.objects.get(id=i)
                    # convert product data to dict with required keys and append dict to list
                    #  serialization
                    ccart.append(({"productname" : product.name,
                            "productid" : product.id,
                            "productunitprice" : self.cart[i]['price'],
                            "productquantity": self.cart[i]['quantity'],
                            "productimage": product.album.default().serialize()}, 
                            (int(self.cart[i]['quantity']) * float(self.cart[i]['price']))
                            ))
        return ccart


    # CREATE CART ITEM OBJECT METHOD 
    # object * string * object -> boolean
    # create new object in user cart item model using the from given data
    def create_ci (self, product, qtt):
        Cart_Item.objects.create(product=product, quantity=qtt, cart=self.user.mycart)
        return True

    # dict -> boolean
    # delete object using product given id 
    # Helper function to delete object in a pattern 
    def delete_objct(item, ucart):
        product= Product.objects.get(id=item)
        # delete object
        Cart_Item.objects.get(product= product, cart=ucart).delete()


    # instance * dict -> boolean
    # create a new or edit existing object in cart_item model  
    def add_to_cart (self, item):
        # is object (Product)
        # load product object from Product model
        product = Product.objects.get(id=int(item['pid']))
        pqtt = int(item['quantity'])
        if self.uli:
            try:
                # is object 
                # single object from cart item model 
                citem = Cart_Item.objects.get(product=product, cart=self.user.mycart)
                # is int 
                # updating incrementing sub value by given int item 
                citem.quantity += pqtt
                citem.save()
                if citem.quantity == 0:
                    citem.delete()
                
            # if previous failed excute this supose element does'nt exist
            except:
                # if product item doesn't exist create new
                self.create_ci(product, pqtt)
        else:
            try:
                qtt = int(self.user['cart'][item['pid']]['quantity'])
                self.user['cart'][item['pid']]['quantity'] = str(qtt + pqtt)
                if (qtt + pqtt) == 0:
                    del self.user['cart'][item['pid']]
            except:
                self.user['cart'][item['pid']] = {'quantity' : str(pqtt), 'price' : str(product.price)}
            
            self.user.save()

        return True

    # dict * dict -> dict
    # takes self variable and json cart update in dict 
    # calculate the difference of quantity btw current car 
    # and update cart, and returne a dict with product id and result
    def update_cart(self, cupdate):
        try:
            self.add_to_cart(cupdate['cart'])
        except:
            if self.uli: 
                cart = self.cart 
            else: 
                cart = self.cart.copy()
            # loop over given update cart and current cart
            for product, item in zip(cupdate['cart'], cart):
                # is int
                # the update cart product quantity
                given = int(product['quantity'])
                # if user login
                if self.uli:
                    # is int
                    # current user cart product quantity
                    current =  item.quantity
                # if user is not logged in
                else:
                    # is int
                    # current cart product quantity
                    current = int(cart[item]['quantity'])
                # is dict 
                # product id and quantity difference 
                result = {'pid': product['pid'],'quantity':(given - current)}
                self.add_to_cart(result)

    def cart_context_process(self):
        # is int 
        # the all page cart update data for top and other use
        items, total = 0, 0
        # int * int -> true
        # calculate the cart qtt and total price
        def calc_cart (qtt, price):
            nonlocal items, total
            items += qtt
            total += (float(qtt)*float(price))

        for i in self.cart:
            if self.uli:
                calc_cart(i.quantity, i.product.price)
            else:
                calc_cart(int(self.cart[i]['quantity']), self.cart[i]['price'])
        
        return items, total