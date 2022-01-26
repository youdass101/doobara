from django.shortcuts import render

# Create your views here.
def blog(request):
    return render(request, "doobarashop/blog.html")

def video(request):
    return render(request, "doobarashop/video.html")

def single_blog_post(request):
    return render(request, "doobarashop/single_blog_post.html")
