from django.db import models

# ImageAlbum is sql django model
# interp. imagealbum link one product id
#  from one side to many images on the other side
class ImageAlbum(models.Model):
    # album name 
    name = models.CharField(max_length=255)

    # list of images -> image
    # return image object that have the default key value true
    def default(self):
        return self.images.filter(default=True).first()
    
    # list of images -> list of images
    # returns the image that fit the width and lenght 
    def thumbnails(self):
        return self.images.filter(width=100, length=100)

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
    alt = models.CharField(max_length=255, blank=True)
    # desctiption is string
    # image description 
    description = models.TextField(blank=True)
    # image is image 
    # the image path
    image = models.ImageField(upload_to= 'static/doobarashop/upload/images')
    # default is boolean 
    # if true the image is the main image for the product 
    default = models.BooleanField(default=False)
    # long is boolean 
    # if true it is for the product singal page long image 
    long = models.BooleanField(default=False)
    # album is model-object 
    # pointer to a specific album object id 
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

    width = models.FloatField(default=100)
    length = models.FloatField(default=100)

    # data to show on admin page 
    def __str__(self):
        return f"{self.name}, {self.album} " 

    # string(url) -> string(url)
    # interp custumize usrl contant 
    def img_path_customize(self, ipath):
        return "/".join(ipath.strip("/").split('/')[2:])

    # image object -> dictionary 
    # take django sql image object and convert data to dictionary 
    def serialize(self):
        return{
            "iname": self.name,
            "ialt": self.alt,
            "idescription": self.description,
            "idefault": self.default,
            "ilong": self.long,
            "iurl": self.img_path_customize(self.image.url)
        }