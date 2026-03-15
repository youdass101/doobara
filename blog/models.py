from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title
    
    def serialize(self):
        return {
            "title": self.title,
            "description": self.description,
            "video_url": self.video_url
        }