from django.shortcuts import render
from .models import *
import objgraph

# Create your views here.
def blog(request):
    objgraph.show_growth()

    return render(request, "blog/blog.html")

def video(request):
    video = Video.objects.all()
    video = [v.serialize() for v in video]

    return render(request, "blog/video.html",{"video": video})

def single_blog_post(request):
    objgraph.show_growth()

    return render(request, "blog/single_blog_post.html")
