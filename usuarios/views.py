from django.shortcuts import render
# users/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Usuario, empleado, empresa
from .forms import EmpleadoForm, creacioUsuarioForm, modificarUsuarioForm

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
    success_url = reverse_lazy('login') 

# UPDATE: Editar un usuario
class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = modificarUsuarioForm
    template_name = 'usuarios/usuario_form.html'
    def get_success_url(self):
        # Redirige a la vista del perfil pasando el ID del usuario actualizado
        return reverse('usuario_detalle', kwargs={'pk': self.object.pk})

# DELETE: Borrar un usuario
class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirmar_baja.html'
    success_url = reverse_lazy('login')

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

class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = empleado
    form_class = EmpleadoForm
    template_name = 'usuarios/empleado/empleado_form.html'

    def form_valid(self, form):
        # Asigna el usuario logueado al objeto sin guardarlo aún en la BBDD
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige de vuelta al perfil del usuario
        return reverse('usuario_detalle', kwargs={'pk': self.request.user.pk})

class EmpleadoUpdateView(UpdateView, LoginRequiredMixin):
    model = empleado
    # Excluimos 'usuario' para que no se pueda transferir el perfil a otra persona al editar
    fields = ['fecha_ingreso', 'cargo', 'cv', 'experiencia']
    template_name = 'usuarios/empleado/empleado_form.html'
    success_url = reverse_lazy('empleado_lista')

class EmpleadoDeleteView(DeleteView, LoginRequiredMixin):
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

class EmpresaCreateView(CreateView, LoginRequiredMixin):
    model = empresa
    fields = ['nombre_empresa', 'descripcion', 'direccion', 'telefono', 'website']
    template_name = 'usuarios/empresa/empresa_form.html'
    def form_valid(self, form):
            # Asigna el usuario logueado al objeto sin guardarlo aún en la BBDD
            form.instance.usuario = self.request.user
            return super().form_valid(form)
    
    def get_success_url(self):
        # Redirige de vuelta al perfil del usuario
        return reverse('usuario_detalle', kwargs={'pk': self.request.user.pk})
    success_url = reverse_lazy('empresa_lista')

class EmpresaUpdateView(UpdateView, LoginRequiredMixin):
    model = empresa
    fields = ['nombre_empresa', 'descripcion', 'direccion', 'telefono', 'website']
    template_name = 'usuarios/empresa/empresa_form.html'
    success_url = reverse_lazy('empresa_lista')

class EmpresaDeleteView(DeleteView, LoginRequiredMixin):
    model = empresa
    template_name = 'usuarios/empresa/empresa_confirmar_baja.html'
    success_url = reverse_lazy('empresa_lista')