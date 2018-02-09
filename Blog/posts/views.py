from django.contrib.auth import login
from django.shortcuts import render, redirect

from users.forms import SignInForm
from .models import Post, Comment
from .forms import SignUpForm


def index(request):
    title = 'Home'
    posts = Post.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    form2 = SignInForm()
    return render(request, 'index.html', {'title': title, 'posts': posts, 'form': form, 'form2': form2})


def post(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'post.html', {'title': post.title, 'post': post})
