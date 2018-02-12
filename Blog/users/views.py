from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

from posts.models import Post
from users.forms import DeleteProfileForm, EditProfileForm, SignInForm


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            try:
                u = User.objects.get(username=request.POST['username'])
            except:
                messages.add_message(request, messages.ERROR,
                                     "Invalid credentials")
                return redirect('index')
            if u and u.check_password(request.POST['password']):
                login(request, u)
            else:
                messages.add_message(request, messages.ERROR,
                                     'Invalid credentials')
        return redirect('index')
    else:
        return redirect('index')


def users(request):
    u = User.objects.all()
    form2 = SignInForm()
    return render(request, 'users.html', {'users': u, 'form2': form2, 'title': 'Users'})


def user(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(user_id=pk, deleted=False)
    form2 = SignInForm()

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm']:
            u = User.objects.get(id=request.user.pk)
            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']
            u.userdetails.bio = form.cleaned_data['bio']
            if form.cleaned_data['image'] is not None:
                u.userdetails.image = form.cleaned_data['image']
            #print('Uspesan (kao) upload.\n\nFile:\t')
            #print(form.cleaned_data['image'])
            u.password = make_password(form.cleaned_data['password'])
            u.save()
            login(request, u)
            return redirect('user', user.pk)
    else:
        form = EditProfileForm(initial={'first_name': user.first_name,
                                        'last_name': user.last_name,
                                        'bio': user.userdetails.bio})

    return render(request, 'user.html', {'user': user, 'posts': posts,
                                         'form': form, 'form2': form2, 'title': user.username})


def delete(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        form = DeleteProfileForm(request.POST)
        if form.is_valid() and User.objects.get(pk=pk).check_password(request.POST['password']):
            u = User.objects.get(pk=pk)
            u.is_active = False
            u.save()
            return redirect('logout')
        else:
            messages.add_message(request, messages.ERROR, 'Wrong password!')
            return render(request, 'deleteprofile.html', {'form': form, 'title': 'Delete your profile'})
    elif request.method == 'GET' and request.user.is_authenticated:
        form = DeleteProfileForm()
        return render(request, 'deleteprofile.html', {'form': form, 'title': 'Delete your profile'})
    else:
        return redirect('index')
