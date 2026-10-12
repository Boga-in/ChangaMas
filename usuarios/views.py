from django.shortcuts import render, redirect
from django.contrib import messages
# users/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Usuario, empleado, empresa
from .forms import EmpleadoForm, creacioUsuarioForm, modificarUsuarioForm, EmpresaForm

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

    #inyecto un dispatch para que no pueda crear un perfil de empleado si ya tiene uno de empleado o empresa
    def dispatch(self, request, *args, **kwargs):
        if getattr(request.user, 'es_empleado', False) or getattr(request.user, 'es_empresa', False):
            messages.warning(request, "Ya tienes un perfil de trabajo registrado. No puedes crear otro.")
            return redirect('usuario_detalle', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Asigna el usuario logueado al objeto sin guardarlo aún en la BBDD
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirige de vuelta al perfil del usuario
        return reverse('usuario_detalle', kwargs={'pk': self.request.user.pk})

class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = empleado
    fields = ['fecha_ingreso', 'cargo', 'cv', 'experiencia']
    template_name = 'usuarios/empleado/empleado_form.html'
    success_url = reverse_lazy('empleado_lista')
    
    # SEGURIDAD: Solo trae el perfil si pertenece al usuario logueado
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = empleado
    template_name = 'usuarios/empleado/empleado_confirmar_baja.html'
    success_url = reverse_lazy('empleado_lista')
    
    # SEGURIDAD
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


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

class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = empresa
    form_class = EmpresaForm # USAMOS EL NUEVO FORMULARIO
    template_name = 'usuarios/empresa/empresa_form.html'

    #mismo dispatch que en empleado para que no pueda crear un perfil de empresa si ya tiene uno de empleado o empresa
    def dispatch(self, request, *args, **kwargs):
        if getattr(request.user, 'es_empleado', False) or getattr(request.user, 'es_empresa', False):
            messages.warning(request, "Ya tienes un perfil de trabajo registrado. No puedes crear otro.")
            return redirect('usuario_detalle', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('usuario_detalle', kwargs={'pk': self.request.user.pk})

class EmpresaUpdateView(LoginRequiredMixin, UpdateView):
    model = empresa
    form_class = EmpresaForm # USAMOS EL NUEVO FORMULARIO
    template_name = 'usuarios/empresa/empresa_form.html'
    success_url = reverse_lazy('empresa_lista')
    
    # SEGURIDAD
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

class EmpresaDeleteView(LoginRequiredMixin, DeleteView):
    model = empresa
    template_name = 'usuarios/empresa/empresa_confirmar_baja.html'
    success_url = reverse_lazy('empresa_lista')
    
    # SEGURIDAD
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)