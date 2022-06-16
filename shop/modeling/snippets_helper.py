from ..models import *

#  -> dict 
# serialized dict for category objects list
def serialized_categories():
    # is list of dict
    # filter all product in the given category, and serizled them in listof dicts
    cats =  Categorie.objects.all()
    scats = [cat.serialize() for cat in cats]
    return scats

# dict -> tuple(dict)
# take a filter form input dict request and return the selection string name 
# this function is for the product shop filter menu, 
def filter_data(form): 
    # is string (both)
    # name of selectd category and orderby filter name
    category = form['category']
    orderby = form['byorder']
    
    # string -> string
    # takes the givin string and compare it with patterns and return the decoded string
    def check_orderby(val):
        # encode and point each given string to required result filter option
        # filter from a to z
        if val == "AZ":
            filter_name = "name"
        # filter backward from z to a 
        elif val == "ZA":
            filter_name = "-name"
        # filter from high to low integer 
        elif val == "lhp":
            filter_name = "price"
        # filter from low to high interger
        elif val == "hlp":
            filter_name = "-price"
        else:
            filter_name = ""
        return filter_name

    # is string
    # order filter value
    filter_option = check_orderby(orderby)
    
    # if catergory string value is (all) default filter only apply   
    if category == "all":
        lop = Product.objects.filter(active=True)
    else:
        lop = Categorie.objects.get(name=category).products.all()
    
   # if orderby string value is (default) no filter is applied 
    if orderby == "default":
        slop = serialize(lop, "main")
    else:
        slop = serialize(lop.order_by(filter_option), "main")

    return slop