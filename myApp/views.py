from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm
from .models import Transaccion
from .forms import TransaccionForm
from django.shortcuts import get_object_or_404
from .forms import PresupuestoForm
from .models import Presupuesto
from .models import Usuarios
from django.contrib import messages


def iniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarSesion.html', {
            'form': AuthenticationForm()
        })
    else:
        usuario = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if usuario is None:
            return render(request, 'iniciarSesion.html', {
                'form': AuthenticationForm(),
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, usuario)
            return redirect('inicio')

def registrarse(request):
    if request.method == 'GET':
        return render(request, 'registrarse.html', {
            'form': CustomUserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario = Usuarios.objects.create_user(
                    username=request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                usuario.save()
                login(request, usuario)
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

# Para cuando queramos validar bien los datos
# def registrarse(request):
#     if request.method == 'GET':
#         return render(request, 'registrarse.html', {'form': CustomUserCreationForm()})
#     else:
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             usuario = form.save()
#             login(request, usuario)
#             return redirect('inicio')
#         return render(request, 'registrarse.html', {'form': form, 'error': 'Error al crear el usuario'})


@login_required
def inicio(request):
    return render(request, 'inicio.html')


@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('iniciarSesion')


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


@login_required
def lista_transacciones(request):
    transacciones = Transaccion.objects.filter(
        usuario=request.user).order_by('-fecha')
    return render(request, 'transacciones/Transacciones.html', {'transacciones': transacciones})


@login_required
def agregar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            nueva_transaccion = form.save(commit=False)
            nueva_transaccion.usuario = request.user
            nueva_transaccion.save()
            messages.success(request, "Transacción añadida correctamente.")
            return redirect('lista_transacciones')
    else:
        form = TransaccionForm()
    return render(request, 'transacciones/Form Transaciones.html', {'form': form})


@login_required
def editar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(
        Transaccion, id=transaccion_id, usuario=request.user)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            messages.success(request, "Transacción modificada correctamente.")
            return redirect('lista_transacciones')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'transacciones/Form Transaciones.html', {'form': form})


@login_required
def eliminar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(
        Transaccion, id=transaccion_id, usuario=request.user)
    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, "Transacción eliminada correctamente.")
        return redirect('lista_transacciones')

    return render(request, 'transacciones/Eliminar Transacion.html', {'transaccion': transaccion})



@login_required
def presupuestos(request):
    presupuestos = Presupuesto.objects.filter(usuario=request.user)

    return render(request, 'presupuestos/presupuestos.html', {
        'presupuestos': presupuestos
    })


@login_required
def agregar_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.save()
            return redirect('presupuestos')
    else:
        form = PresupuestoForm()

    return render(request, 'presupuestos/agregar_presupuesto.html', {
        'form': form,
    })


@login_required
def editar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(
        Presupuesto, id=presupuesto_id, usuario=request.user)

    if request.method == 'POST':
        form = PresupuestoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            return redirect('presupuestos')
    else:
        form = PresupuestoForm(instance=presupuesto)

    return render(request, 'presupuestos/editar_presupuesto.html', {
        'form': form,
    })


@login_required
def eliminar_presupuesto(request, presupuesto_id):
    presupuesto = get_object_or_404(
        Presupuesto, id=presupuesto_id, usuario=request.user)

    if request.method == 'POST':
        presupuesto.delete()
        return redirect('presupuestos')

    return render(request, 'presupuestos/eliminar_presupuesto.html', {
        'presupuesto': presupuesto
    })
