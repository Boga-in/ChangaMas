from django.shortcuts import render, redirect
from django.contrib import messages
# users/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Usuario, empleado, empresa
from .forms import EmpleadoForm, creacioUsuarioForm, modificarUsuarioForm, EmpresaForm

#MIXINS
class SoloPropietarioMixin(UserPassesTestMixin):
    """
    Mixin genérico para asegurar que solo el dueño del objeto (o un admin)
    pueda acceder a una CBV de actualización o eliminación.
    """
    # Atributo por defecto que apunta al usuario en el modelo (puedes cambiarlo si tu FK se llama 'user')
    user_field_name = 'usuario' 

    def test_func(self):
        user = self.request.user

        # 1. Si es superusuario o staff, permitimos el acceso total por seguridad/administración
        if user.is_superuser or user.is_staff:
            return True

        # 2. Obtenemos el objeto actual que la CBV va a editar/eliminar
        obj = self.get_object()
        
        # 3. Buscamos al dueño evaluando diferentes estructuras comunes en Django:
        owner = getattr(obj, self.user_field_name, None)
        
        # Caso A: El obj extiende a User nativo de Django)
        if obj == user:
            return True

        # Caso B: Si tu modelo tiene una relación directa con empleado u otro campo personalizado
        if obj.__class__.__name__ == 'empleado' and obj.usuario == user:
            return True
        if obj.__class__.__name__ == 'empresa' and obj.usuario == user:
            return True
        return False

    def handle_no_permission(self):
        # Opcional: Redirigir con un mensaje de error o lanzar un 403 limpio
        return super().handle_no_permission()

class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        # Django evalúa automáticamente si el usuario es staff o superusuario
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

# READ: Lista de todos los usuarios
class UsuarioListView(LoginRequiredMixin, SoloAdminMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_lista.html'
    context_object_name = 'usuarios' # Nombre de la variable en el HTML
    def test_func(self):
        # Devuelve True solo si el usuario que hace la petición es superusuario
        return self.request.user.is_superuser

# READ: Detalle de un usuario específico
class UsuarioDetailView(SoloPropietarioMixin, DetailView):
    model = Usuario
    template_name = 'usuarios/usuario_detalle.html'
    context_object_name = 'usuario'

# CREATE: Crear un usuario nuevo
class UsuarioCreateView(SoloPropietarioMixin, CreateView):
    model = Usuario
    form_class = creacioUsuarioForm
    template_name = 'usuarios/usuario_form.html'
    # Redirige a la lista después de crear exitosamente
    success_url = reverse_lazy('login') 

# UPDATE: Editar un usuario
class UsuarioUpdateView(LoginRequiredMixin, SoloPropietarioMixin, UpdateView):
    model = Usuario
    form_class = modificarUsuarioForm
    template_name = 'usuarios/usuario_form.html'
    def get_success_url(self):
        # Redirige a la vista del perfil pasando el ID del usuario actualizado
        return reverse('usuario_detalle', kwargs={'pk': self.object.pk})

# DELETE: Borrar un usuario
class UsuarioDeleteView(LoginRequiredMixin, SoloPropietarioMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirmar_baja.html'
    success_url = reverse_lazy('login')

# ==========================================
# CRUD PARA EMPLEADOS
# ==========================================

class EmpleadoListView(LoginRequiredMixin, SoloAdminMixin, ListView):
    model = empleado
    template_name = 'usuarios/empleado/empleado_lista.html'
    context_object_name = 'empleados'

class EmpleadoDetailView(SoloPropietarioMixin, DetailView):
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

class EmpleadoUpdateView(LoginRequiredMixin, SoloPropietarioMixin, UpdateView):
    model = empleado
    fields = ['fecha_ingreso', 'cargo', 'cv', 'experiencia']
    template_name = 'usuarios/empleado/empleado_form.html'
    def get_success_url(self):
                # Redirige al detalle del empleado pasando el ID del usuario actualizado
                return reverse('empleado_detalle', kwargs={'pk': self.object.pk})
    # SEGURIDAD: Solo trae el perfil si pertenece al usuario logueado
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

class EmpleadoDeleteView(LoginRequiredMixin, SoloPropietarioMixin, DeleteView):
    model = empleado
    template_name = 'usuarios/empleado/empleado_confirmar_baja.html'
    success_url = reverse_lazy('empleado_lista')
    
    # SEGURIDAD
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)


# ==========================================
# CRUD PARA EMPRESAS
# ==========================================

class EmpresaListView(LoginRequiredMixin, SoloAdminMixin, ListView):
    model = empresa
    template_name = 'usuarios/empresa/empresa_lista.html'
    context_object_name = 'empresas'

class EmpresaDetailView(SoloPropietarioMixin, DetailView):
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

class EmpresaUpdateView(LoginRequiredMixin, SoloPropietarioMixin, UpdateView):
    model = empresa
    form_class = EmpresaForm # USAMOS EL NUEVO FORMULARIO
    template_name = 'usuarios/empresa/empresa_form.html'
    def get_success_url(self):
            # Redirige al detalle de la empresa pasando el ID del usuario actualizado
            return reverse('empresa_detalle', kwargs={'pk': self.object.pk})
    
    # SEGURIDAD
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

class EmpresaDeleteView(LoginRequiredMixin, SoloPropietarioMixin, DeleteView):
    model = empresa
    template_name = 'usuarios/empresa/empresa_confirmar_baja.html'
    success_url = reverse_lazy('empresa_lista')
    
    # SEGURIDAD
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)