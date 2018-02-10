from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import SignInForm
from .models import Post, Comment
from .forms import SignUpForm


def index(request):
    title = 'Home'
    posts = Post.objects.filter(deleted=False).order_by('created_at').reverse()
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
    post = get_object_or_404(Post, pk=pk, deleted=False)
    comments = Comment.objects.filter(post_id=pk).order_by('id')
    return render(request, 'post.html', {'title': post.title, 'post': post, 'comments': comments})


def posts(request):
    return render(request, 'posts.html', {'posts': Post.objects.filter(deleted=False)})