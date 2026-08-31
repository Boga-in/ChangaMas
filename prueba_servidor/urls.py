
from django.contrib import admin
from django.urls import path
from changamas.views import crear_publicacion, inicio, listar_publicaciones

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear/', crear_publicacion, name='crear_publicacion'),
    path('listar/', listar_publicaciones, name='listar_publicaciones'),
    path('', inicio, name='inicio'),
]
