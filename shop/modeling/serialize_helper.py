from .. import models as md
import markdown


def _get_primary_image(product):
    primary = product.images.filter(thumbnail=True).first() or product.images.first()
    if not primary:
        return None
    return {
        "url": primary.image.url,
        "alt_text": primary.alt_text or product.name,
        "thumbnail": primary.thumbnail,
    }


def _get_all_images(product):
    return [
        {
            "url": image.image.url,
            "alt_text": image.alt_text or product.name,
            "thumbnail": image.thumbnail,
        }
        for image in product.images.all()
    ]


#  -> dict 
# serialized dict for category objects list
def serialized_categories():
    # is list of dict
    # filter all product in the given category, and serizled them in listof dicts
    # (loc: shop.models )
    cats =  md.Categorie.objects.all()
    scats = [cat.serialize() for cat in cats]
    return scats

# listofobjects * string -> dict
# serialize given list of products, method can be either main and everything else has the same result
def serialize(lop, method):
    # function is a method in models file for product model | (loc: shop.models )
    return [object.serialize(method) for object in lop]

# model_object * string - > dictionary 
# reutrning a dictionary of specified keys in a given object model (the engine of product serialize method)
def product_serialize(object, tag):
    inventory = object.get_inventory_data()

    # is list of dict | (loc: shop.models )
    # all category object connected to the given object 
    category_list = [cat.serialize() for cat in object.category.all()]

    image = _get_primary_image(object)
    all_images = _get_all_images(object)
    variant_options = [
        {
            "id": variant.id,
            "title": variant.title,
            "default": variant.is_default,
        }
        for variant in object.variants.filter(active=True).order_by("sort_order")
    ]


    # is a Dictionary
    # if loading in carousel no details data loaded  
    if tag == 'main':
        # do not load inactive products (loc: shop.models/images )
        if object.active:
            return {
            "pid": object.id,
            "id": object.id,
            "pname": object.name,
            "title": object.name,
            "slug": object.slug,
            "brand": object.brand,
            "sku": object.sku,
            "url": object.get_absolute_url(),
            "pprice": object.price,
            "price": object.price,
            "currency": object.currency,
            "in_stock": inventory["in_stock"],
            "can_purchase": inventory["can_purchase"],
            "is_preorder": inventory["is_preorder"],
            "availability_label": inventory["availability_label"],
            "cart_cta_label": inventory["cart_cta_label"],
            "quantity": inventory["quantity"],
            "pcategory": category_list,
            "category": category_list,
            "pmainimage": image,
            "main_image": image,
            # !!! HAVE TO BE REMOVED FROM HTML CODE IN ANY IF CONFITION
            "pactive" : object.active,
            "active": object.active,
            "system": object.is_system
        }
    # if loading in single product with full details data loaded
    else:
        short_description_lines = [line.strip() for line in object.short_description.splitlines()
            if line.strip()
        ]
        long_description = markdown.markdown(object.description)
        
        return {
            "pid": object.id,
            "id": object.id,
            "pname": object.name,
            "title": object.name,
            "slug": object.slug,
            "brand": object.brand,
            "sku": object.sku,
            "url": object.get_absolute_url(),
            "pprice": object.price,
            "price": object.price,
            "currency": object.currency,
            "in_stock": inventory["in_stock"],
            "can_purchase": inventory["can_purchase"],
            "is_preorder": inventory["is_preorder"],
            "availability_label": inventory["availability_label"],
            "cart_cta_label": inventory["cart_cta_label"],
            "quantity": inventory["quantity"],
            "pshortdescription": short_description_lines,
            "short_description": short_description_lines,
            "plongdescription": long_description,
            "long_description": long_description,
            "pvideo": object.video,
            "pcreationdate": object.created_time,
            "pcategory": category_list,
            "category": category_list,
            "pmainimage": image,
            "main_image": image,
            "pallimages": all_images,
            "all_images": all_images,
            "system": object.is_system,
            "variant": object.variant,
            "pvariant": variant_options,
            "variant_options": variant_options,
            "dimensions": object.dimensions,
            "weight": object.weight,
        }
