from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


def home(request):
    post = Post.objects.all()
    return HttpResponse(post)
