from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuarios
from .models import Transaccion
from .models import Presupuesto


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Ingresa un correo válido.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar contraseña"
    )

    class Meta:
        model = Usuarios
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }



class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        help_text="Ingresa un correo válido.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        required=True,
        help_text="Ingresa un nombre de usuario único.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        required=False,
        help_text="Ingresa tu nombre (opcional).",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=False,
        help_text="Ingresa tu apellido (opcional).",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuarios
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        current_user = self.instance
        if Usuarios.objects.filter(username=username).exclude(pk=current_user.pk).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )




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
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'})
        }
