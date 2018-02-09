from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Comment


def home(request):
    title = 'Home'
    posts = Post.objects.all()
    return render(request, 'index.html', {'title': title, 'posts': posts})


def post(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'post.html', {'title': post.title, 'post': post})
