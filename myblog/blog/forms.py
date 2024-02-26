from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import *

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["email", "phone", "password1", "password2"]

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['phone', 'password']

class CreateArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ["name", "desc", "img"]

class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['msg']
