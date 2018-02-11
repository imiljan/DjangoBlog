"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from posts.views import comment, create, index, like, post, posts, search
from users.views import delete, signin, user, users


from django.conf.urls import include, url
import debug_toolbar


urlpatterns = [
    path('', index, name='index'),
    path('signin/', signin, name='signin'),
    path('search/', search, name='search'),
    path('users/<int:pk>/', user, name='user'),
    path('posts/', posts, name='posts'),
    path('posts/<int:pk>/', post, name='post'),
    path('posts/<int:pk>/like', like, name='like'),
    path('posts/<int:pk>/comment', comment, name='comment'),
    path('posts/create', create, name='create'),
    path('users/', users, name='users'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('users/<int:pk>/delete', delete, name='delete'),
    path('admin/', admin.site.urls),

    url(r'^__debug__/', include(debug_toolbar.urls)),

]
