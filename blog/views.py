from django.shortcuts import render
import objgraph

# Create your views here.
def blog(request):
    objgraph.show_growth()

    return render(request, "blog/blog.html")

def video(request):
    objgraph.show_growth()

    return render(request, "blog/video.html")

def single_blog_post(request):
    objgraph.show_growth()

    return render(request, "blog/single_blog_post.html")
