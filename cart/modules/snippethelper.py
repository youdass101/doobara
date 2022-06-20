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

# list(object) -> integer
# take list of address and return ID of the one that have default as true 
def default_address(lod):
    for i in lod:
        if i['default']:
            return int(i['id'])
        else:
            return 0