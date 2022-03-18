from ..models import *

# listofobjects * string -> dict
# serialize given list of products 
def serialize(loo, method):
    return [object.serialize(method) for object in loo]