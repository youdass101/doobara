from ..models import *

# dict -> tuple(dict)
# take a filter form input dict request and return the selection string name 
# this function is for the product shop filter menu, 
def filter_data(form): 
    # is string (both) (from html submited request)
    # name of selectd category and orderby filter name
    category = form['category']
    # orderby = form['byorder']
    filter_option = form['byorder']
    
    # (loc: shop.models)
    # if catergory string value is (all) default filter only apply   
    if category == "all":
        lop = Product.objects.filter(active=True)
    else:
        lop = Categorie.objects.get(name=category).products.all()
    
   # loc: shop.modeling.serialize_helper 
   # if orderby string value is (default) no filter is applied 
    if filter_option == "default":
        slop = serialize(lop, "main")
    else:
        slop = serialize(lop.order_by(filter_option), "main")

    return slop