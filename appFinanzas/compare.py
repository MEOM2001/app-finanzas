from ast import Import
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from matplotlib.style import context
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm
from .models import Transaccion
from .forms import TransaccionForm
from django.shortcuts import get_object_or_404
from .forms import PresupuestoForm
from .models import Presupuesto
from .models import Usuarios
from django.contrib import messages
from django.http.response import JsonResponse
from django.db.models import Sum
from myApp.models import Presupuesto
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
import matplotlib.pyplot as plt
import base64

# Vista para renderizar la página de inicio con estadísticas
@login_required
def inicio(request):
    # Obtener el total de ingresos
    total_ingresos = Transaccion.objects.filter(usuario=request.user, tipo='Ingreso').aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    # Obtener el total de egresos
    total_egresos = Transaccion.objects.filter(usuario=request.user, tipo='egreso').aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    # Preparar datos para el gráfico de ingresos vs. egresos
    labels_ingresos_egresos = ['Ingresos', 'Egresos']
    data_ingresos_egresos = [total_ingresos, total_egresos]

    # Obtener el total de transacciones por tipo
    transacciones_por_tipo = Transaccion.objects.filter(usuario=request.user).values('tipo').annotate(total=Sum('cantidad'))
    labels_tipos = [item['tipo'] for item in transacciones_por_tipo]
    data_tipos = [item['total'] for item in transacciones_por_tipo]

    context = {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'labels_ingresos_egresos': labels_ingresos_egresos,
        'data_ingresos_egresos': data_ingresos_egresos,
        'labels_tipos': labels_tipos,
        'data_tipos': data_tipos,
    }
    return render(request, 'inicio.html', context)

@login_required
def get_chart(request):
    # Sumar ingresos y egresos
    total_ingresos = Transaccion.objects.filter(usuario=request.user, tipo='ingreso').aggregate(Sum('cantidad'))['cantidad__sum'] or 0
    total_egresos = Transaccion.objects.filter(usuario=request.user, tipo='egreso').aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    # Sumar por tipo
    transacciones_por_tipo = Transaccion.objects.filter(usuario=request.user).values('tipo').annotate(total=Sum('cantidad'))
    labels_tipos = [item['tipo'] for item in transacciones_por_tipo]
    data_tipos = [item['total'] for item in transacciones_por_tipo]

    chart = {
        'labels_ingresos_egresos': ['Ingresos', 'Egresos'],
        'data_ingresos_egresos': [total_ingresos, total_egresos],
        'labels_tipos': labels_tipos,
        'data_tipos': data_tipos,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resumen_financiero.pdf"'
    template = get_template(template_path) # type: ignore
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response