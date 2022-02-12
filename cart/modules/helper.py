from ..models import *

# dict * dict -> boolean (event)
# add item in "item" to loggedin user "in request" cart "in models"
# if user cart object exist add item else create table object
# if item exist in cart adjust value else create item object  
def user_add_to_cart (request, item, product):
    
    # load current loggedin user object model 
    user = request.user
    try:
        # if use have object cart
        user.mycart
        try:
            # If product item object already exist adjust
            citem = Cart_Item.objects.get(product=product, cart=user.mycart)
            citem.quantity += int(item['quantity'])
            citem.save()
        except:
            # if product item doesn't exist create new
            Cart_Item.objects.create(product=product, quantity=item['quantity'], cart=user.mycart)
    except:
        # If user cart object doesn't exist create new one
        cart = Cart.objects.create(user=user)
        Cart_Item.objects.create(product=product, quantity=item['quantity'], cart=user.mycart)

# dict * dict -> dict
# if session doesn't exist create new one 
# save or adjust cart data in session dict with given item
def session_add_to_cart (request, item, product):
    # if session deosn't exist create new
    if not request.session:
        request.session.save()

    price = product.price
    session = request.session
    try:
        session['cart'][item['pid']]['quantity'] = str(item['quantity'])
    except:
        try:
            session['cart'][item['pid']] = {'quantity' : str(item["quantity"]), 'price' : str(price)}
        except:
            session['cart'] = {}
            session['cart'][item['pid']] = {'quantity' : str(item["quantity"]), 'price' : str(price)}

    print(session['cart'])

