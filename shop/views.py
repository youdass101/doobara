from django.shortcuts import render
from .models import *

# Created modules to manage shop page functions
from .modeling.serialize_helper import *
from .modeling.filter_helper import *

# request -> render (url * dict)
# caller: Navigation home (domain index page)
# render the index html template and page data 
def index(request):
    # is int
    # number of items that will show in index featured bar
    items_in_featrued = 5
    # is list of dict | (loc: shop.modeling.serialize_helper (shop.models ))
    # all products objects with feature TRUE, in serialized dict
    slop = serialize(Product.objects.filter(featured=True), "main")
    return render(request, "shop/index.html", {"lop":slop[:items_in_featrued]})

# request -> render (url  * dict)
# caller: navigation shop
# render the shop html template and shop page data
def shop(request):
    # is list of dict | (loc: shop.modeling.serialize_helper (shop.models))
    # all products objects with active TRUE, in serialized dict
    slop = serialize(Product.objects.filter(active=True), "main")
    # is list of dict | (loc: shop.modeling.serialize_helper)
    # filter all product in the given category, and serizled them in listof dicts
    scats =  serialized_categories()

    return render(request, "shop/shop.html", {"lop":slop, "cats":scats})

# I still use this function instead of orderby function for index nav category because here I can use less process
# request * string -> render (url * dict)
# caller: category navigation at index page
# render shop html template and filtered product objects data serialized in list of dict
def filtering(request, locat):
    # is list of dict | (loc: shop.modeling.serialize_helper)
    # filter all product in the given category, and serizled them in listof dicts (from snippets helper)
    scats =  serialized_categories()
    # is dict | (loc: shop.modeling.serialize_helper)
    # serialized product list filterd by targeted cat (from helper)
    slop = serialize(Categorie.objects.get(name=locat).products.all(), "main")

    return render(request, "shop/shop.html", {"lop":slop, "cats":scats})

# request * string -> render (url * dict)  
# caller: product icon anywhere
# render single product html template with and given product data dict
def single_product(request, locat):
    # is dict | (loc: shop.models)
    # given product name, prodcut object serialized dict (using models)
    product = Product.objects.get(name=locat).serialize("all")

    return render(request, "shop/single_product.html", {"product": product})


# request -> render(url * dict)
# filter products that contain same pattern or chars in name 
# caller: search widget in navigation and mobile footer
def search(request):
    if request.method == "POST":
        # is dict | HTML request data submition
        # form input data dictionary (from html)
        form = request.POST['keyword']
        # is dict | (loc: shop.modeling.serialize_helper)
        # this is serialized list of the filtered keyword products (from helper file )
        slop = serialize(Product.objects.filter(name__contains=form), "main")
         # is list of dict | (loc: shop.modeling.serialize_helper)
        # filter all product in the given category, and serizled them in listof dicts (from snippets-helper)
        scats =  serialized_categories()

    return render(request, "shop/shop.html", {"lop": slop, "cats":scats})

# request -> render (url * dict)
# caller: shp catergory tab (form)
# filter, sort product list
def orderby(request):
    # if html request method is POST 
    if request.method == "POST":
        # is dict | HTML request data submited
        # Posted data with html request 
        form = request.POST
        # is dict | (loc: shop.modeling.filter_helper)
        # serialized list of product filterd by givin filter keyowrds
        slop = filter_data(form)
        # is list of dict | (loc: shop.modeling.serialize_helper)
        # filter all product in the given category, and serizled them in listof dicts
        scats =  serialized_categories()

    return render(request, "shop/shop.html", {"lop": slop, "cats":scats})


# request -> render(url)
# caller: main nav and fotter
# render contact us html template
def contactus(request):
    return render(request, "shop/contactus.html")
