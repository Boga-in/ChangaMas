from django.shortcuts import render
# users/views.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Usuario, empleado, empresa
from .forms import creacioUsuarioForm, modificarUsuarioForm

# READ: Lista de todos los usuarios
class UsuarioListView(UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_lista.html'
    context_object_name = 'usuarios' # Nombre de la variable en el HTML
    def test_func(self):
        # Devuelve True solo si el usuario que hace la petición es superusuario
        return self.request.user.is_superuser

# READ: Detalle de un usuario específico
class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'usuarios/usuario_detalle.html'
    context_object_name = 'usuario'

# CREATE: Crear un usuario nuevo
class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = creacioUsuarioForm
    template_name = 'usuarios/usuario_form.html'
    # Redirige a la lista después de crear exitosamente
    success_url = reverse_lazy('usuario_lista') 

# UPDATE: Editar un usuario
class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = modificarUsuarioForm
    template_name = 'usuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_lista')

# DELETE: Borrar un usuario
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirmar_baja.html'
    success_url = reverse_lazy('usuario_lista')

# ==========================================
# CRUD PARA EMPLEADOS
# ==========================================

class EmpleadoListView(ListView):
    model = empleado
    template_name = 'usuarios/empleado/empleado_lista.html'
    context_object_name = 'empleados'

class EmpleadoDetailView(DetailView):
    model = empleado
    template_name = 'usuarios/empleado/empleado_detalle.html'
    context_object_name = 'empleado'

class EmpleadoCreateView(CreateView):
    model = empleado
    # Incluimos 'usuario' para que puedas asignarle el perfil a una cuenta existente
    fields = ['usuario', 'fecha_ingreso', 'cargo', 'cv', 'experiencia']
    template_name = 'usuarios/empleado/empleado_form.html'
    success_url = reverse_lazy('empleado_lista')

class EmpleadoUpdateView(UpdateView):
    model = empleado
    # Excluimos 'usuario' para que no se pueda transferir el perfil a otra persona al editar
    fields = ['fecha_ingreso', 'cargo', 'cv', 'experiencia']
    template_name = 'usuarios/empleado/empleado_form.html'
    success_url = reverse_lazy('empleado_lista')

class EmpleadoDeleteView(DeleteView):
    model = empleado
    template_name = 'usuarios/empleado/empleado_confirmar_baja.html'
    success_url = reverse_lazy('empleado_lista')


# ==========================================
# CRUD PARA EMPRESAS
# ==========================================

class EmpresaListView(ListView):
    model = empresa
    template_name = 'usuarios/empresa/empresa_lista.html'
    context_object_name = 'empresas'

class EmpresaDetailView(DetailView):
    model = empresa
    template_name = 'usuarios/empresa/empresa_detalle.html'
    context_object_name = 'empresa'

class EmpresaCreateView(CreateView):
    model = empresa
    fields = ['usuario', 'nombre_empresa', 'descripcion', 'direccion', 'telefono', 'website']
    template_name = 'usuarios/empresa/empresa_form.html'
    success_url = reverse_lazy('empresa_lista')

class EmpresaUpdateView(UpdateView):
    model = empresa
    fields = ['nombre_empresa', 'descripcion', 'direccion', 'telefono', 'website']
    template_name = 'usuarios/empresa/empresa_form.html'
    success_url = reverse_lazy('empresa_lista')

class EmpresaDeleteView(DeleteView):
    model = empresa
    template_name = 'usuarios/empresa/empresa_confirmar_baja.html'
    success_url = reverse_lazy('empresa_lista')