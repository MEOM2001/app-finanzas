from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaccion
from .models import Presupuesto


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Ingresa un correo válido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, help_text="Ingresa un correo válido.")

    class Meta:
        model = User
        fields = ['email']


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'cantidad', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['nombre', 'descripcion', 'precio', 'fecha', 'website']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
