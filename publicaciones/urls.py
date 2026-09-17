from django.urls import path
from . import views

urlpatterns = [
    # Las rutas aquí se sumarán a lo que diga el proyecto principal
    path('crear/', views.crear_publicacion, name='crear_publicacion'),
    path('lista/', views.listar_publicaciones, name='listar_publicaciones'),
    path('', views.inicio, name='inicio'),
]