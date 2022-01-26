from . import views
from django.urls import path


urlpatterns=[   
    # Blog carousel page
    path("blog", views.blog, name="blog"),
    # Video Carousel page
    path("video", views.video, name="video"),
    # Single Blog Post page
    path("single_blog_post", views.single_blog_post, name="single_blog_post"),
]