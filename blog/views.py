from django.shortcuts import render

# Create your views here.
def blog(request):
    return render(request, "blog/blog.html")

def video(request):
    return render(request, "blog/video.html")

def single_blog_post(request):
    return render(request, "blog/single_blog_post.html")
