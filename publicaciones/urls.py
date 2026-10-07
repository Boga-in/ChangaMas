from django.urls import path
from .views import (
    InicioView,
    PublicacionCreateView,
    PublicacionListView,
    PublicacionDetailView,
    PublicacionUpdateView,
    PublicacionDeleteView,
    MisPublicacionesListView,
    CrearPerfilTrabajoView
)

app_name = 'publicaciones'

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('mis_publicaciones/', MisPublicacionesListView.as_view(), name='mis_publicaciones'),
    path('publicaciones/', PublicacionListView.as_view(), name='lista'),
    path('crear/', PublicacionCreateView.as_view(), name='crear'),
    path('<int:pk>/', PublicacionDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', PublicacionUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', PublicacionDeleteView.as_view(), name='eliminar'),
    path('crear_perfil_trabajo/', CrearPerfilTrabajoView, name='crear_perfil_trabajo'),
]