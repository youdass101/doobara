from django.db import models

# ImageAlbum is sql django model
# interp. imagealbum link one product id
#  from one side to many images on the other side
class ImageAlbum(models.Model):
    # album name string
    name = models.CharField(max_length=255)

    # list of images -> image
    # return image object that have the default key value true
    def default(self):
        return self.images.filter(thumbnail=True).first()
    
    # list of images -> list of images
    # returns the image that fit the width and lenght 
    def thumbnails(self):
        # it can be for now all instead filter
        return self.images.filter()

    # data to show on admin page 
    def __str__(self):
        return f"{self.name} " 

# image is Sql django model
# interp each object contain image informations and url
class Image(models.Model):
    # name is string
    # image title
    name = models.CharField(max_length=255)
    # alt is string
    # image short interpretation 
    alt_text = models.CharField(max_length=255, blank=True)
    # image is image 
    # the image path
    image = models.ImageField(upload_to= 'static/doobarashop/upload/images')
    # default is boolean 
    # if true the image is the main image for the product 
    thumbnail = models.BooleanField(default=False)  # True if this is a thumbnail image
    # album is model-object 
    # pointer to a specific album object id 
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

    # data to show on admin page 
    def __str__(self):
        return f"{self.name}, {self.album} " 

    # string(url) -> string(url)
    # interp custumize usrl contant 
    def img_path_customize(self):
        return "/".join(self.image.url.strip("/").split('/')[1:])

    # image object -> dictionary 
    # take django sql image object and convert data to dictionary 
    def serialize(self):
        return{
            "iname": self.name,
            "ialt": self.alt_text,
            "idefault": self.thumbnail,
            "iurl": self.img_path_customize()
        }