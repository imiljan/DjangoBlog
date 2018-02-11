from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, CreatePostForm
from posts.models import Comment, Like, Post
from users.forms import SignInForm, SignUpForm


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
    return render(request, 'index.html', {'title': title, 'posts': posts,
                                          'form': form, 'form2': form2})


def post(request, pk):
    p = get_object_or_404(Post, pk=pk, deleted=False)
    p.views += 1
    p.save()
    comments = Comment.objects.filter(post_id=pk).order_by('id')
    user = User.objects.get(pk=post.user_id.id)
    flag = False
    try:
        Like.objects.get(user_id=request.user.id, post_id=p.id)
        flag = True
    except:
        pass
    form2 = SignInForm()
    comment_form = CommentForm()
    return render(request, 'post.html', {'title': post.title, 'post': post,
                                         'comments': comments, 'user': user,
                                         'flag': flag, 'form2': form2,
                                         'comment_form': comment_form})


def posts(request):
    form2 = SignInForm()
    p = Post.objects.filter(deleted=False).order_by('created_at')
    return render(request, 'posts.html', {'posts': p, 'form2': form2})


def like(request, pk):
    if request.method == 'POST':
        Like.objects.create(user_id=request.user, post_id=Post.objects.get(pk=pk))
        p = Post.objects.get(pk=pk)
        p.likes += 1
        p.save()
        return JsonResponse({'message': 'Success'})


def create(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            p = Post.objects.create(title=request.POST['title'],
                                    body=request.POST['body'],
                                    user_id=request.user)
            return redirect('post', p.id)
    else:
        form = CreatePostForm()
    return render(request, 'createpost.html', {'form': form})


def comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            p = Post.objects.get(pk=pk)
            c = Comment.objects.create(body=request.POST['body'],
                                       user_id=request.user, post_id=p)
            return JsonResponse({'message': c.body})
    else:
        return JsonResponse({'message': 'error'})
