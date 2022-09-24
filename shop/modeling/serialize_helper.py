from .. import models as md


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
    # is list of dict | (loc: shop.models )
    # all category object connected to the given object 
    category_list = [cat.serialize() for cat in object.category.all()]
    # image is image dict
    # return the default product image if the object album is empty return none to avoid error
    try:
        # if product have an album
        # (loc: shop.images )
        image = object.album.default().serialize()
    except:
        # else return None
        image = None

    # -> list of dictionary
    # convert a list of object to a list of dictionary usng helpers
    # return all images in a product album if no obejcts exist return none to avoid erors
    def allimages():
        try:
            # (loc: shop.images )
            return [i.serialize() for i in object.album.thumbnails()]
        except:
            return None

    # -> ListOfDict
    # return product variants product lod data
    def variants():
        # (loc: shop.models )
        if object.variant_list:
            # Can't use serialize because to avoid an infinit loop of self recall at this line
            return [{"title" : var.variant_name, "price":int(var.price), "id": var.id} 
                    for var in object.variant_list.products.all()]
        else:
            return None


    # is a Dictionary
    # if loading in carousel no details data loaded  
    if tag == 'main':
        # do not load inactive products (loc: shop.models/images )
        if object.active:
            return {
            "pid": object.id,
            "pname": object.name,
            "pprice": object.price,
            "pcategory": category_list,
            "pmainimage": image,
            # !!! HAVE TO BE REMOVED FROM HTML CODE IN ANY IF CONFITION
            "pactive" : object.active,
        }
    # if loading in single product with full details data loaded
    else:
        return {
            "pid": object.id,
            "pname": object.name,
            "pprice": object.price,
            "pshortdescription": object.short_description,
            "plongdescription": object.long_description,
            "pvideo": object.video,
            "pcreationdate": object.created_time,
            "pcategory": category_list,
            "pmainimage": image,
            "pallimages": allimages(),
            "pvariant" : variants(),
            "pvname" : object.variant_name
        }

