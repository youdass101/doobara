from django.shortcuts import get_object_or_404, render
from .models import *
from django.urls import reverse
from django.db.models import Q

# Created modules to manage shop page functions
from .modeling.serialize_helper import *
from .modeling.filter_helper import *

def _serialize_main_products(queryset):
    """
    Shared list-page serializer path.
    Keeps prefetch + serialization logic in one place so maintenance is easier.
    """
    return serialize(queryset.prefetch_related("category", "images"), "main")


def _shop_page_response(request, products):
    """
    Shared shop page response builder.
    Unifies repeated context wiring used by shop/filter/search/orderby views.
    """
    scats = serialized_categories()
    return render(request, "shop/shop.html", {"lop": products, "cats": scats})


# request -> render (url * dict)
# caller: Navigation home (domain index page)
# render the index html template and page data 
def index(request):
    # is int
    # number of items that will show in index featured bar
    items_in_featrued = 7
    # is list of dict | (loc: shop.modeling.serialize_helper (shop.models ))
    # all products objects with feature TRUE, in serialized dict
    
    cards = Hero_Card.objects.filter(active=True)
    cards = [card.serialize() for card in cards]
    # PERF: prefetch related records consumed by serializer (category/images) to reduce N+1 queries.
    slop = _serialize_main_products(Product.objects.filter(featured=True))
    return render(request, "shop/index.html", {"lop":slop[:items_in_featrued], "cards": cards})

# request -> render (url  * dict)
# caller: navigation shop
# render the shop html template and shop page data
def shop(request):
    # is list of dict | (loc: shop.modeling.serialize_helper (shop.models))
    # all products objects with active TRUE, in serialized dict
    # PERF: serializer touches category/images for each product; prefetch once.
    slop = _serialize_main_products(Product.objects.filter(active=True))
    return _shop_page_response(request, slop)

# I still use this function instead of orderby function for index nav category because here I can use less process
# request * string -> render (url * dict)
# caller: category navigation at index page
# render shop html template and filtered product objects data serialized in list of dict
def filtering(request, locat):
    # PERF: category page serializes each product with category/images; prefetch in one query set.
    slop = _serialize_main_products(Categorie.objects.get(name=locat).products.all())
    return _shop_page_response(request, slop)

# request * string -> render (url * dict)  
# caller: product icon anywhere
# render single product html template with and given product data dict
def single_product(request, locat=None, slug=None):
    lookup_key = slug or locat
    parent_product = get_object_or_404(Product, Q(slug=lookup_key) | Q(name=lookup_key))

    # is dict | (loc: shop.models)
    # given product name, prodcut object serialized dict (using models)
    product = parent_product.serialize("all")

    variants_qs = (
        parent_product.variants.filter(active=True)
        .prefetch_related("images", "package_items__included_product__images")
        .order_by("sort_order")
    )

    tier_priority = {"advanced": 0, "basic": 1, "pro": 2}
    variants = []
    default_variant = None

    for variant in variants_qs:
        variant_inventory = variant.get_inventory_data()
        thumb = variant.images.filter(thumbnail=True).first() or variant.images.first()
        images = [
            {"url": image.image.url, "alt_text": image.alt_text}
            for image in variant.images.all()
        ]
        package_items = []
        for package_item in variant.package_items.all():
            included_thumb = package_item.included_product.images.filter(thumbnail=True).first() or package_item.included_product.images.first()
            package_items.append(
                {
                    "name": package_item.included_product.name,
                    "url": package_item.included_product.get_absolute_url(),
                    "qty": package_item.quantity,
                    "thumbnail": included_thumb.image.url if included_thumb else None,
                }
            )

        variant_payload = {
            "id": variant.id,
            "tier": variant.tier,
            "title": variant.title,
            "short_description": variant.short_description,
            "description": variant.description,
            "price": float(variant.price),
            "sale_price": float(variant.sale_price) if variant.sale_price else None,
            "currency": variant.currency,
            "in_stock": variant_inventory["in_stock"],
            "availability_label": variant_inventory["availability_label"],
            "quantity": variant_inventory["quantity"],
            "thumbnail": thumb.image.url if thumb else None,
            "images": images,
            "package_items": package_items,
            "is_default": variant.is_default,
            "sort_order": variant.sort_order,
        }
        variants.append(variant_payload)

        if variant.is_default and not default_variant:
            default_variant = variant_payload

    if variants and not default_variant:
        default_variant = sorted(
            variants,
            key=lambda item: (tier_priority.get(item["tier"], 99), item["sort_order"]),
        )[0]

    return render(
        request,
        "shop/single_product.html",
        {
            "product": product,
            "variants": variants,
            "default_variant": default_variant,
        },
    )


# request -> render(url * dict)
# filter products that contain same pattern or chars in name 
# caller: search widget in navigation and mobile footer
def search(request):
    if request.method == "POST":
        # is dict | HTML request data submition
        # form input data dictionary (from html)
        form = request.POST['keyword']
        # PERF: search uses the same serializer path as shop list views.
        slop = _serialize_main_products(Product.objects.filter(name__contains=form))
        return _shop_page_response(request, slop)

    return _shop_page_response(request, [])

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
        # NOTE: filter_data still owns sort/filter rules; keep logic centralized.
        slop = filter_data(form)
        return _shop_page_response(request, slop)

    return _shop_page_response(request, [])


# request -> render(url)
# caller: main nav and fotter
# render contact us html template
def contactus(request):
    return render(request, "shop/contactus.html")
