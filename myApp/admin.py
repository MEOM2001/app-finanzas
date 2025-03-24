from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios

admin.site.register(Usuarios, UserAdmin)