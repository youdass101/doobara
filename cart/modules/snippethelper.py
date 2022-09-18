from shop.models import *
# This a helper mini functions for cart application 



# NOTES FOR OPTIMIZATION 
# scart_data_setup function can be replace with the session cart itself 
# but the session cart pattern should be custumized to match the cds function output pattern


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
                "productunitprice" : cart[i]['price'],
                "productquantity": cart[i]['quantity'],
                "productimage": product.album.default().serialize()}, 
                (int(cart[i]['quantity']) * float(cart[i]['price']))
                ))

    return lst


    