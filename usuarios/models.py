from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    dni = models.CharField(max_length=8)
    telefono = models.CharField(max_length=15)
    es_admin_general = models.BooleanField(default=False)

    def __str__(self):
        return self.username