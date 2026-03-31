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


def _format_price_range(min_price, max_price):
    """
    Format listing price consistently with existing two-decimal display style.
    Returns either "$ X.XX" or "$ X.XX - $ Y.YY" when range exists.
    """
    if min_price is None or max_price is None:
        return "$ 0.00"
    if min_price == max_price:
        return f"$ {float(min_price):.2f}"
    return f"$ {float(min_price):.2f} - $ {float(max_price):.2f}"


def _get_selectable_price_bounds(product):
    """
    Compute min/max price for selectable options on listing cards.
    - System products use active system variants.
    - Non-system products with normal variants use active normal variants.
    - Simple products fall back to product-level price.
    """
    # Use .all() so view-level prefetching can satisfy this without extra DB hits.
    if product.is_system:
        prices = [
            variant.sale_price if variant.sale_price else variant.price
            for variant in product.variants.all()
            if variant.active
        ]
    else:
        prices = [
            variant.sale_price if variant.sale_price else variant.price
            for variant in product.normal_variants.all()
            if variant.active
        ]

    if not prices:
        base_price = product.sale_price if product.sale_price else product.price
        return base_price, base_price

    return min(prices), max(prices)


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
    # Normal product variants are intentionally separate from system variants.
    active_normal_variants = [
        variant for variant in object.normal_variants.all() if variant.active
    ]
    variant_options = [
        {
            "id": variant.id,
            "title": variant.title,
            "default": variant.is_default,
            "price": variant.price,
            "sale_price": variant.sale_price,
            "short_description": variant.short_description,
            "image": variant.image.url if variant.image else None,
        }
        for variant in sorted(active_normal_variants, key=lambda item: item.sort_order)
    ]
    # Shop cards must force option selection for configurable products.
    requires_option_selection = object.is_system or bool(variant_options)
    # Listing price reflects selectable option price range when needed.
    price_min, price_max = _get_selectable_price_bounds(object)
    price_display = _format_price_range(price_min, price_max)


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
            "price_display": price_display,
            "price_min": price_min,
            "price_max": price_max,
            "requires_option_selection": requires_option_selection,
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
            "price_display": price_display,
            "price_min": price_min,
            "price_max": price_max,
            "requires_option_selection": requires_option_selection,
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
