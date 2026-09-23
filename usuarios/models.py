from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    dni = models.CharField(max_length=8, unique=True)
    telefono = models.CharField(max_length=15)
    es_admin_general = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='media/fotos_perfil/', null=True, blank=True)
    def __str__(self):
        return self.username

class empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    cargo = models.CharField(max_length=100)
    cv = models.FileField(upload_to='media/cv/', null=True, blank=True)
    experiencia = models.TextField()
    def __str__(self):
        return self.usuario.username

class empresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    website = models.URLField()
    def __str__(self):
        return self.nombre_empresa