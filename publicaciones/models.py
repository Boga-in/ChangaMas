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

class busquedaEmpleo(models.Model):
    id_empleado = models.ForeignKey(empleado, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    habilidades = models.ManyToManyField(
            Habilidad, 
            blank=True, 
            related_name='empleados'
        )
    def __str__(self):
        return self.titulo
    
class busquedaEmpleado(models.Model):
    id_empresa = models.ForeignKey(empresa, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    habilidades_requeridas = models.ManyToManyField(
            Habilidad, 
            blank=True, 
            related_name='ofertas'
        )
    def __str__(self):
        return self.titulo



class Publicacion(models.Model):
    oferta = models.ForeignKey(busquedaEmpleado, on_delete=models.CASCADE, null=True, blank=True)
    busqueda = models.ForeignKey(busquedaEmpleo, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', null=True, blank=True)
    descripcion = models.TextField()
    duracion = models.CharField(max_length=100, null=True, blank=True)
    urgencia = models.CharField(max_length=100, choices=[('urgente', 'Urgente'), ('normal', 'Normal')], default='normal', null=True, blank=True)
    lugar = models.CharField(max_length=100, null=True, blank=True)
    foto = models.ImageField(upload_to='media/fotos_trabajo/', null=True, blank=True)

    def __str__(self):
        return self.titulo