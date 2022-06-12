from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .modeling.helper import *

# request -> render (url * dict)
# render the index html template and page data 
def index(request):
    # isvlist of dict
    # all products objects with feature TRUE, in serialized dict
    slop = serialize(Product.objects.filter(featured=True), "main")
    return render(request, "shop/index.html", {"lop":slop[:5]})

# request -> render (url * dict)
# render the shop html template and shop page data
def shop(request):
    # is list of dict
    # all products objects with active TRUE, in serialized dict
    slop = serialize(Product.objects.filter(active=True), "main")
    cats =  Categorie.objects.all()
    scats = [cat.serialize() for cat in cats]

    return render(request, "shop/shop.html", {"lop":slop, "cats":scats})

# request * string -> render (url * dict)
# render shop html template and filtered product objects data serialized in list of dict
def filtering(request, locat):
    # is list of dict
    # filter all product in the given category, and serizled them in listof dicts
    cats =  Categorie.objects.all()
    scats = [cat.serialize() for cat in cats]

    slop = serialize(Categorie.objects.get(name=locat).products.all(), "main")

    return render(request, "shop/shop.html", {"lop":slop, "cats":scats})

# request * string -> render (url * dict)
# render single product html template with and given product data dict
def single_product(request, locat):
    # is dict
    # given product name, prodcut object serialized dict
    product = Product.objects.get(name=locat).serialize("all")
    return render(request, "shop/single_product.html", {"product": product})

# request -> render(url)
# render contact us html template
def contactus(request):
    return render(request, "shop/contactus.html")


# request -> render(url)
def search(request):
    if request.method == "POST":
        # is dict
        # form input data dictionary 
        form = request.POST['keyword']
        # is dict 
        # this is serialized list of the filtered keyword products
        slop = serialize(Product.objects.filter(name__contains=form), "main")
        cats =  Categorie.objects.all()
        scats = [cat.serialize() for cat in cats]


        
    return render(request, "shop/shop.html", {"lop": slop, "cats":scats})


def orderby(request):
    if request.method == "POST":
        form = request.POST
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

        cats =  Categorie.objects.all() 
        scats = [cat.serialize() for cat in cats]

    return render(request, "shop/shop.html", {"lop": slop, "cats":scats})



