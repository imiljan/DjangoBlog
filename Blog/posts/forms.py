from django import forms

from .models import Comment, Post


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
