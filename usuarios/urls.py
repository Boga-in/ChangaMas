# users/urls.py
from django.urls import path
from .views import (
    EmpleadoCreateView, EmpleadoDeleteView, EmpleadoDetailView, EmpleadoListView, EmpleadoUpdateView,
    EmpresaCreateView, EmpresaDeleteView, EmpresaDetailView, EmpresaListView, EmpresaUpdateView,
    UsuarioCreateView, UsuarioDeleteView, UsuarioDetailView, UsuarioListView, UsuarioUpdateView
)

urlpatterns = [
    # Rutas para Usuarios
    path('', UsuarioListView.as_view(), name='usuario_lista'),
    path('<int:pk>/', UsuarioDetailView.as_view(), name='usuario_detalle'),
    path('nuevo/', UsuarioCreateView.as_view(), name='usuario_crear'),
    path('<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('<int:pk>/eliminar/', UsuarioDeleteView.as_view(), name='usuario_eliminar'),
    # Rutas para Empleados
    path('empleados/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleados/<int:pk>/', EmpleadoDetailView.as_view(), name='empleado_detail'),
    path('empleados/nuevo/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/<int:pk>/editar/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', EmpleadoDeleteView.as_view(), name='empleado_delete'),

    # Rutas para Empresas
    path('empresas/',   EmpresaListView.as_view(), name='empresa_list'),
    path('empresas/<int:pk>/', EmpresaDetailView.as_view(), name='empresa_detail'),
    path('empresas/nuevo/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresas/<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresas/<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa_delete'),
]