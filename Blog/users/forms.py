from django import forms
from django.contrib.auth.models import User


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']
