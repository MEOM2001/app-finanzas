from django.db import models
from django.contrib.auth.models import User


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.cantidad}"
    

class Presupuesto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre