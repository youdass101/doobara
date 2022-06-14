from django.shortcuts import render
from .models import *

# Created modules to manage shop page functions
from .modeling.helper import *
from .modeling.snippets_helper import *

# request -> render (url * dict)
# render the index html template and page data 
def index(request):
    # is int
    # number of items that will show in index featured bar
    items_in_featrued = 5
    # isvlist of dict
    # all products objects with feature TRUE, in serialized dict
    slop = serialize(Product.objects.filter(featured=True), "main")
    return render(request, "shop/index.html", {"lop":slop[:items_in_featrued]})

# request -> render (url * dict)
# render the shop html template and shop page data
def shop(request):
    # is list of dict
    # all products objects with active TRUE, in serialized dict
    slop = serialize(Product.objects.filter(active=True), "main")
    # is list of dict
    # filter all product in the given category, and serizled them in listof dicts
    scats =  serialized_categories()

    return render(request, "shop/shop.html", {"lop":slop, "cats":scats})

# request * string -> render (url * dict)
# render shop html template and filtered product objects data serialized in list of dict
def filtering(request, locat):
    # is list of dict
    # filter all product in the given category, and serizled them in listof dicts (from snippets helper)
    scats =  serialized_categories()
    # is dict
    # serialized product list filterd by targeted cat (from helper)
    slop = serialize(Categorie.objects.get(name=locat).products.all(), "main")

    return render(request, "shop/shop.html", {"lop":slop, "cats":scats})

# request * string -> render (url * dict)
# render single product html template with and given product data dict
def single_product(request, locat):
    # is dict
    # given product name, prodcut object serialized dict (using models)
    product = Product.objects.get(name=locat).serialize("all")

    return render(request, "shop/single_product.html", {"product": product})


# request -> render(url)
def search(request):
    if request.method == "POST":
        # is dict
        # form input data dictionary (from html)
        form = request.POST['keyword']
        # is dict 
        # this is serialized list of the filtered keyword products (from helper file )
        slop = serialize(Product.objects.filter(name__contains=form), "main")
         # is list of dict
        # filter all product in the given category, and serizled them in listof dicts (from snippets-helper)
        scats =  serialized_categories()

    return render(request, "shop/shop.html", {"lop": slop, "cats":scats})


def orderby(request):
    # if html request method is POST 
    if request.method == "POST":
        # is dict
        # Posted data with html request 
        form = request.POST
        # is dict 
        # serialized list of product filterd by givin filter keyowrds
        slop = filter_data(form)
        # is list of dict
        # filter all product in the given category, and serizled them in listof dicts
        scats =  serialized_categories()

    return render(request, "shop/shop.html", {"lop": slop, "cats":scats})


# request -> render(url)
# render contact us html template
def contactus(request):
    return render(request, "shop/contactus.html")
