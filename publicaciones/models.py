from django.db import models
from usuarios.models import empleado, empresa
from django.conf import settings  # <-- Usamos settings

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    empresa = models.ForeignKey(empresa, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(empleado, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', null=True, blank=True)
    descripcion = models.TextField()
    duracion = models.CharField(max_length=100, null=True, blank=True)
    urgencia = models.CharField(max_length=100, choices=[('urgente', 'Urgente'), ('normal', 'Normal')], default='normal', null=True, blank=True)
    lugar = models.CharField(max_length=100, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_trabajo/', null=True, blank=True)
    titulo = models.CharField(max_length=200, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    habilidades = models.ManyToManyField(
            Habilidad, 
            blank=True, 
            related_name='requerimientos'
        )
    def __str__(self):
        # Si tiene oferta, muestra el título de la oferta, si no, el de la búsqueda
        if self.empresa:
            return f"Oferta: {self.empresa.nombre_empresa}"
        elif self.empleado:
            return f"Búsqueda: {self.empleado.usuario.nombre}"
        return {self.id}