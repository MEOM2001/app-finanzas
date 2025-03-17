from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Ingresa un correo válido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Ingresa un correo válido.")

    class Meta:
        model = User
        fields = ['email']