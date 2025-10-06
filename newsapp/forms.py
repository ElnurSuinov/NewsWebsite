from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import News


class RegForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["news_title", "main_text", "news_category", "news_image"]
