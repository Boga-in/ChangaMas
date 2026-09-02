from django.db import models
from django.conf import settings  # <-- Usamos settings

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='media/fotos_trabajo/')
    # <-- Ahora apuntamos a AUTH_USER_MODEL
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo