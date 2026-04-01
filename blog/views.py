from django.shortcuts import render
from .models import *


# Create your views here.
def blog(request):
    return render(request, "blog/blog.html")


def video(request):
    video = Video.objects.all()
    video = [v.serialize() for v in video]

    return render(request, "blog/video.html", {"video": video})


def single_blog_post(request):
    return render(request, "blog/single_blog_post.html")


def privacy_policy(request):
    return render(request, "blog/privacy_policy.html")


def shipping_policy(request):
    return render(request, "blog/shipping_policy.html")


def user_deletion_instruction(request):
    return render(request, "blog/user_deletion_instruction.html")
