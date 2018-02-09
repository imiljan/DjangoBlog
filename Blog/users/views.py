from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from posts.models import Post
from users.forms import SignInForm


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            try:
                u = User.objects.get(username=request.POST['username'])
            except:
                messages.add_message(request, messages.ERROR, "Invalid credentials")
                return redirect('index')
            login(request, u)
        return redirect('index')
    else:
        return redirect('index')


def users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def user(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(user_id=pk)
