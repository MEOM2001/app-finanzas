from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.iniciarSesion, name='iniciar sesion'),
    path('inicio/', views.inicio, name='inicio'),
    path('perfil/', views.perfil, name='perfil'),
    path('cerrarSesion/', views.cerrarSesion, name='cerrar sesion'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('transacciones/', views.lista_transacciones, name='lista_transacciones'),
    path('transacciones/nueva/', views.agregar_transaccion,
         name='agregar_transaccion'),
    path('transacciones/editar/<int:transaccion_id>/',
         views.editar_transaccion, name='editar_transaccion'),
    path('transacciones/eliminar/<int:transaccion_id>/',
         views.eliminar_transaccion, name='eliminar_transaccion'),
    path('presupuestos/', views.presupuestos, name='presupuestos'),
    path('agregar_presupuesto/', views.agregar_presupuesto, name='agregar_presupuesto'),
    path('editar_presupuesto/<int:presupuesto_id>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('eliminar_presupuesto/<int:presupuesto_id>/', views.eliminar_presupuesto, name='eliminar presupuesto')
]