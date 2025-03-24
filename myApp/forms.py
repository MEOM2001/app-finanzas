from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuarios
from .models import Transaccion
from .models import Presupuesto


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Ingresa un correo válido.")

    class Meta:
        model = Usuarios
        fields = ("username", "first_name", "last_name","email", "password1", "password2")


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, help_text="Ingresa un correo válido.")
    username = forms.CharField(
        required=True, help_text="Ingresa un nombre de usuario único.")
    first_name = forms.CharField(
        required=False, help_text="Ingresa tu nombre (opcional).")
    last_name = forms.CharField(
        required=False, help_text="Ingresa tu apellido (opcional).")

    class Meta:
        model = Usuarios
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        current_user = self.instance
        
        if Usuarios.objects.filter(username=username).exclude(pk=current_user.pk).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        
        return username


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
