from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gastosIngresos/', views.gastosIngresos, name='gastos ingresos'),
    path('', views.iniciarSesion, name='iniciar sesion'),
    path('inicio/', views.inicio, name='inicio'),
    path('perfil/', views.perfil, name='perfil'),
    path('presupuestos/', views.presupuestos, name='presupuestos'),
    path('cerrarSesion/', views.cerrarSesion, name='cerrar sesion'),
    path('registrarse/', views.registrarse, name='registrarse')
]
