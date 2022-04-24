from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .modeling.helper import *
import objgraph

# request -> render (url * dict)
# render the index html template and page data 
def index(request):
    # isvlist of dict
    # all products objects with feature TRUE, in serialized dict
    slop = serialize(Product.objects.filter(featured=True), "main")
    objgraph.get_leaking_objects()
    return render(request, "shop/index.html", {"lop":slop[:5]})

# request -> render (url * dict)
# render the shop html template and shop page data
def shop(request):
    # is list of dict
    # all products objects with active TRUE, in serialized dict
    slop = serialize(Product.objects.filter(active=True), "main")
    objgraph.get_leaking_objects()

    return render(request, "shop/shop.html", {"lop":slop})

# request * string -> render (url * dict)
# render shop html template and filtered product objects data serialized in list of dict
def filtering(request, locat):
    # is list of dict
    # filter all product in the given category, and serizled them in listof dicts
    slop = serialize(Categorie.objects.get(name=locat).products.all(), "main")
    objgraph.show_growth()

    return render(request, "shop/shop.html", {"lop":slop})

# request * string -> render (url * dict)
# render single product html template with and given product data dict
def single_product(request, locat):
    # is dict
    # given product name, prodcut object serialized dict
    product = Product.objects.get(name=locat).serialize("all")
    objgraph.get_leaking_objects()


    return render(request, "shop/single_product.html", {"product": product})

# request -> render(url)
# render contact us html template
def contactus(request):
    objgraph.show_growth()

    return render(request, "shop/contactus.html")