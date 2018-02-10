from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=255, required=True,
                            widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(required=True)
    body = forms.CharField(widget=forms.Textarea(), required=True)

    class Meta:
        model = Post
        fields = ['title', 'body']


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ['body', ]
