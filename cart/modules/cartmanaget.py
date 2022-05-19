from ..models import *

# dict -> boolean
# if user in session and have items in cart and the logging in user cart model 
# is already empty move the session cart object and create them in cart model..
def sessiontousercart (request):
    