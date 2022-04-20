from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class Auth(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
