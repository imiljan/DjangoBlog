from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404

from posts.models import Post
from users.forms import DeleteProfileForm, EditProfileForm, SignInForm


def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            u = authenticate(username=request.POST['username'],
                             password=request.POST['password'])
            if u is not None:
                login(request, u)
                messages.add_message(request, messages.INFO,
                                     'Welcome {}'.format(u))
            else:
                messages.add_message(request, messages.ERROR,
                                     "Invalid credentials!")
    return redirect('index')


def users(request):
    u = User.objects.all()
    form2 = SignInForm()
    return render(request, 'users.html', {'users': u, 'form2': form2,
                                          'title': 'Users'})


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
            u.set_password(form.cleaned_data['password'])
            u.save()
            update_session_auth_hash(request, u)
            messages.add_message(request, messages.INFO, "Profile edited!")
            return redirect('user', user.pk)
    else:
        form = EditProfileForm(initial={'first_name': user.first_name,
                                        'last_name': user.last_name,
                                        'bio': user.userdetails.bio})

    return render(request, 'user.html', {'user': user, 'posts': posts,
                                         'form': form, 'form2': form2,
                                         'title': user.username})


@login_required
def delete(request, pk):
    if request.method == 'POST':
        form = DeleteProfileForm(request.POST)
        u = get_object_or_404(User, pk=pk)
        if form.is_valid() and u.check_password(request.POST['password']):
            u.is_active = False
            u.save()
            return redirect('logout')
        else:
            messages.add_message(request, messages.ERROR, 'Wrong password!')
            return render(request, 'deleteprofile.html',
                          {'form': form, 'title': 'Delete your profile'})
    elif request.method == 'GET':
        form = DeleteProfileForm()
        return render(request, 'deleteprofile.html',
                      {'form': form, 'title': 'Delete your profile'})
    else:
        return redirect('index')
