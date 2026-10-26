from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, empleado, empresa

# Opcional pero recomendado para ver los campos de contraseñas y permisos ordenados:
admin.site.register(Usuario, UserAdmin)