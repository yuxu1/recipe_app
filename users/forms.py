from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AppUser


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=50, help_text='Note: This will be visible to others.')
    bio = forms.CharField(widget=forms.Textarea, max_length=1000, required=False, help_text='Provide a brief summary of yourself (optional)')
    pic = forms.ImageField(label='Profile Picture', required=False, help_text='optional')

    class Meta:
        model = User
        fields = ('username', 'name', 'bio', 'pic', 'password1', 'password2')