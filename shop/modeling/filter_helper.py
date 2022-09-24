from ..models import *

# dict -> tuple(dict)
# take a filter form input dict request and return the selection string name 
# this function is for the product shop filter menu, 
def filter_data(form): 
    # is string (both) (from html submited request)
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

    # is string | Local fuunction called
    # order filter value
    filter_option = check_orderby(orderby)
    # (loc: shop.models)
    # if catergory string value is (all) default filter only apply   
    if category == "all":
        lop = Product.objects.filter(active=True)
    else:
        lop = Categorie.objects.get(name=category).products.all()
    
   # loc: shop.modeling.serialize_helper 
   # if orderby string value is (default) no filter is applied 
    if orderby == "default":
        slop = serialize(lop, "main")
    else:
        slop = serialize(lop.order_by(filter_option), "main")

    return slop