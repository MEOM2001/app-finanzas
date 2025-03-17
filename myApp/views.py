from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm


def iniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarSesion.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciarSesion.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('inicio')


def registrarse(request):
    if request.method == 'GET':
        return render(request, 'registrarse.html', {
            'form': CustomUserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('inicio')
            except IntegrityError:
                return render(request, 'registrarse.html', {
                    'form': CustomUserCreationForm,
                    'error': 'El usuario ya existe'
                })
            except ValueError as e:
                return render(request, 'registrarse.html', {
                    'form': CustomUserCreationForm,
                    'error': str(e)
                })
        return render(request, 'registrarse.html', {
            'form': CustomUserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })


@login_required
def gastosIngresos(request):
    return render(request, 'gastosIngresos.html')


@login_required
def presupuestos(request):
    return render(request, 'presupuestos.html')


@login_required
def inicio(request):
    return render(request, 'inicio.html')


@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('iniciar sesion')


@login_required
def perfil(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'perfil.html', {
        'form': form
    })