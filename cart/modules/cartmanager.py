from ..models import *
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
# project files
from .snippethelper import *

# When user login 
# Migrate session cart to user cart
@receiver(user_logged_in)
def cart_after_login(request, **kwargs):
    userorsession(request)
    cart_migration(request)

# !!! MOVE TO snippethelper file !!! ?
# dict -> boolean 
# move session cart item to use cart data if user cart is empty
def cart_migration(request):
    # is list of dict
    # get given reg-user sub instance cart (connected instance) - sub instance items in cart instance
    user_cart = request.user.mycart.items.all()
    # is list of dick 
    # list of dictionary with product cart item data for none login user
    session_cart = request.session['cart']
    # in case the reg-user cart is empty and the session cart have data
    # than we should migrate the session data to login user connected cart model sub data 
    if cart_empty(user_cart) and (not cart_empty(session_cart)):
        for item in session_cart:
            # is dict
            # cart item data with patttern that fit the cm method
            itemdetail = {'pid': item, 'quantity': session_cart[item]['quantity']}
            # is instance 
            # cartmanager class 
            cart = CartManager(request)
            cart.add_to_cart(itemdetail)





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
    # CART DATA RENDER METHOD
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
            # using helper from snippetherlper to setup the data structer template
            ccart = scart_data_setup(self.cart, [])
        return ccart


    # instance * dict -> boolean
    # ADD TO CART METHOD 
    # create a new or edit existing object in cart_item model  
    def add_to_cart (self, item):
        # is object (Product)
        # load product object from Product model
        product = Product.objects.get(id=int(item['pid']))
        # is int 
        # given quantity of items to be added to cart
        pqtt = int(item['quantity'])

        # IF USER LOGGED IN 
        if self.uli:
            try:
                # is object 
                # single object from cart item model 
                citem = Cart_Item.objects.get(product=product, cart=self.user.mycart)
                # is int 
                # updating incrementing sub value by given int item 
                citem.quantity += pqtt
                citem.save()
                # if item in cart qtt is 0 delete it
                if citem.quantity == 0:
                    citem.delete()
                
            # if previous failed excute this supose element does'nt exist
            except:
                # if product item doesn't exist create new record
                Cart_Item.objects.create(product=product, quantity=pqtt, cart=self.user.mycart)

        # SESSION USER CART
        else:
            try:
                # is Int
                # quantity of a spesific product id in session cart 
                qtt = int(self.user['cart'][item['pid']]['quantity'])
                # is string 
                # user session cart dict
                self.user['cart'][item['pid']]['quantity'] = str(qtt + pqtt)
                # if item in cart qtt is 0 delete it
                if (qtt + pqtt) == 0:
                    del self.user['cart'][item['pid']]
            # key item doesn't exist so create a new one 
            except:
                self.user['cart'][item['pid']] = {'quantity' : str(pqtt)}
            
            self.user.save()

        return True

    # dict * dict -> dict
    # UPDATE CART DATA METHOD 
    # takes self variable and json cart update in dict 
    # calculate the difference of quantity btw current car 
    # and update cart, and returne a dict with product id and result
    def update_cart(self, cupdate):
        try:
            # if delete button is used on page
            self.add_to_cart(cupdate['cart'])
        # if change in qtt is made
        except:
            # if user is logged in point to the instance cart
            if self.uli: 
                cart = self.cart 
            # user not logged in so take a copy of session dict
            else:
                # get a copy of dict session  
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
                # edit cart item using add to cart method
                self.add_to_cart(result)
