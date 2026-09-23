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
    path('empleados/', EmpleadoListView.as_view(), name='empleado_lista'),
    path('empleados/<int:pk>/', EmpleadoDetailView.as_view(), name='empleado_detalle'),
    path('empleados/nuevo/', EmpleadoCreateView.as_view(), name='empleado_crear'),
    path('empleados/<int:pk>/editar/', EmpleadoUpdateView.as_view(), name='empleado_editar'),
    path('empleados/<int:pk>/eliminar/', EmpleadoDeleteView.as_view(), name='empleado_eliminar'),

    # Rutas para Empresas
    path('empresas/',   EmpresaListView.as_view(), name='empresa_lista'),
    path('empresas/<int:pk>/', EmpresaDetailView.as_view(), name='empresa_detalle'),
    path('empresas/nuevo/', EmpresaCreateView.as_view(), name='empresa_crear'),
    path('empresas/<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa_editar'),
    path('empresas/<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa_eliminar'),
]