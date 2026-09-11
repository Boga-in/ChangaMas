from django.urls import path
from .views import (
    PublicacionCreateView,
    PublicacionListView,
    PublicacionDetailView,
    PublicacionUpdateView,
    PublicacionDeleteView,
)

app_name = 'publicaciones'

urlpatterns = [
    path('', PublicacionListView.as_view(), name='lista'),
    path('crear/', PublicacionCreateView.as_view(), name='crear'),
    path('<int:pk>/', PublicacionDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', PublicacionUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', PublicacionDeleteView.as_view(), name='eliminar'),
]