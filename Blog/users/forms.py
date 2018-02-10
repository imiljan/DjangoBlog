from betterforms.multiform import MultiModelForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import UserDetails


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class EditProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea())
    image = forms.FileField(widget=forms.FileInput(), required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm = forms.CharField(widget=forms.PasswordInput())
