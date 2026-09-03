from django.urls import path
from . import views

urlpatterns = [
    # La ruta raíz de esta app mostrará la vista de inicio
    path('', views.inicio, name='inicio'),
]