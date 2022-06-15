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
def filter_data(form): 
    # is string (both)
    # name of selectd category and orderby filter name
    category = form['category']
    orderby = form['byorder']

    if orderby == "AZ":
        ob = "name"
    elif orderby == "ZA":
        ob = "-name"
    elif orderby == "lhp":
        ob = "price"
    elif orderby == "hlp":
        ob = "-price"
    else:
        ob = ""
        
    if category == "all":
        lop = Product.objects.filter(active=True)
    else:
        lop = Categorie.objects.get(name=category).products.all()
    

    if orderby == "default":
        slop = serialize(lop, "main")
    else:
        slop = serialize(lop.order_by(ob), "main")

    return slop