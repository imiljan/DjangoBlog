from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm, CreatePostForm
from posts.models import Comment, Like, Post
from users.forms import SignInForm, SignUpForm


def index(request):
    title = 'Home'
    p = Post.objects.filter(deleted=False).order_by('created_at').reverse()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.INFO, 'Welcome to our Blog!')
            return redirect('index')
    else:
        form = SignUpForm()
    form2 = SignInForm()
    return render(request, 'index.html', {'title': title, 'posts': p,
                                          'form': form, 'form2': form2})


def post(request, pk):
    p = get_object_or_404(Post, pk=pk, deleted=False)
    p.views += 1
    p.save()
    comments = Comment.objects.filter(post_id=pk).order_by('id')
    user = User.objects.get(pk=p.user_id.id)
    flag = False
    try:
        Like.objects.get(user_id=request.user.id, post_id=p.id)
        flag = True
    except:
        pass
    form2 = SignInForm()
    comment_form = CommentForm()
    return render(request, 'post.html', {'title': p.title, 'post': p,
                                         'comments': comments, 'user': user,
                                         'flag': flag, 'form2': form2,
                                         'comment_form': comment_form})


def posts(request):
    form2 = SignInForm()
    p = Post.objects.filter(deleted=False).order_by('created_at').reverse()
    return render(request, 'posts.html', {'posts': p, 'form2': form2, 'title': 'Posts'})


@login_required
def like(request, pk):
    if request.method == 'POST':
        Like.objects.create(user_id=request.user, post_id=Post.objects.get(pk=pk))
        p = Post.objects.get(pk=pk)
        p.likes += 1
        p.save()
        return JsonResponse({'message': 'success'})
    else:
        return redirect('post', pk)


@login_required
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
    return render(request, 'createpost.html', {'form': form, 'title': 'Create a post'})


@login_required
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
    return redirect('post', pk)


def search(request):
    try:
        q = request.GET['q']
    except:
        return redirect('index')
    p = Post.objects.filter(Q(title__contains=q) | Q(body__contains=q))\
        .order_by('created_at')
    u = User.objects.filter(Q(username__contains=q) | Q(first_name__contains=q) |
                            Q(last_name__contains=q) | Q(email__contains=q))\
        .order_by('username')
    return render(request, 'searchresults.html', {'posts': p, 'users': u,
                                                  'title': q + ' - Search'})
