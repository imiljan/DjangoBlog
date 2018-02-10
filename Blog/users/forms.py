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


class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super(EditUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm')

        if password != confirm:
            raise ValidationError("Passwords don't match!")


class EditUserDetailsForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(), required=False)
    bio = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = UserDetails
        fields = ['bio', 'image']


class EditProfileForm(MultiModelForm):
    form_classes = {
        'user': EditUserForm,
        'user_details': EditUserDetailsForm
    }
