from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import request
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView

from .forms import PublicacionForm
from .models import Publicacion, ReportePublicacion
from django.contrib.auth.decorators import login_required

#Funcion para verificar si el usuario es visor o admin
def es_visor_o_admin(user):
    return user.is_superuser or user.groups.filter(name='visores').exists() or user.is_staff

class InicioView(ListView):
    model = Publicacion
    context_object_name = 'publicaciones'
    paginate_by = 10

    def get_template_names(self):
        if self.request.user.is_authenticated:
            # Plantilla para usuarios logueados (Dashboard / Feed de publicaciones)
            return ['publicaciones/muro.html']
        
        # Plantilla para visitantes (Landing informativa de ChangaMas)
        return ['publicaciones/inicio.html']

    def get_queryset(self):
        # 1. Obtenemos la consulta base (todos los empleados)
        queryset = super().get_queryset().exclude(reportes__estado='pendiente').distinct()

        # 2. Capturamos lo que el usuario escribió en el input name="q"
        termino_busqueda = self.request.GET.get('q')
        
        # 3. Si el usuario escribió algo, aplicamos el filtro
        if termino_busqueda:
            # __icontains busca coincidencias parciales sin importar mayúsculas/minúsculas
            queryset = queryset.filter(titulo__icontains=termino_busqueda)
            
        return queryset

class PublicacionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'publicaciones/crear_publicacion.html'
    success_url = reverse_lazy('publicaciones:mis_publicaciones')
    success_message = '¡La publicación se creó correctamente!'

    # Agregado para redirigir a los usuarios que no tienen perfil de Empleado o Empresa deje una publicación de prueba en mi base para ver lo del 404
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, 'es_empleado', False) and not getattr(request.user, 'es_empresa', False):
            messages.warning(request, "Debes crear un perfil de Empleado o Empresa antes de publicar.")
            return redirect('publicaciones:crear_perfil_trabajo')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.es_empleado:
            form.instance.empleado = self.request.user.empleado
        elif self.request.user.es_empresa:
            form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)
    
#Vista basada en clase para ver una publicacion (Read)
class PublicacionDetailView(LoginRequiredMixin,DetailView):
    model = Publicacion
    template_name = 'publicaciones/detalle_publicacion.html'
    context_object_name = 'publicacion'

#Vista basada en clase para Listar las publicaciones
class PublicacionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Publicacion
    template_name = 'publicaciones/listar_publicaciones.html'
    paginate_by = 10
    # Función de validación para el UserPassesTestMixin
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='visores').exists() or user.is_staff

    # Sobrescribimos este método para enviar múltiples querysets a la plantilla
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Publicaciones con reportes pendientes (con optimización prefetch_related)
        context['pubs_reportadas'] = Publicacion.objects.filter(
            reportes__estado='pendiente'
        ).prefetch_related('reportes__usuario').distinct()

        # 2. Publicaciones normales (que no tienen reportes pendientes)
        context['pubs_normales'] = Publicacion.objects.exclude(
            reportes__estado='pendiente'
        ).distinct()
        
        return context

class MisPublicacionesListView(LoginRequiredMixin, ListView):
    model = Publicacion
    template_name = 'publicaciones/mis_publicaciones.html'
    context_object_name = 'publicaciones'

    def get_queryset(self):
        # Filtra únicamente las publicaciones pasándole la instancia del PERFIL, no del usuario
        if self.request.user.es_empleado:
            return Publicacion.objects.filter(empleado=self.request.user.empleado).order_by('-id')
            
        elif self.request.user.es_empresa:
            return Publicacion.objects.filter(empresa=self.request.user.empresa).order_by('-id')
            
        # Buena práctica: Si el usuario no tiene perfil aún, no devolvemos nada para evitar errores
        return Publicacion.objects.none()
        
#Vista basada en clase para Editar una publicacion (Update)
# IMPORTANTE: Ya no hereda de UserPassesTestMixin
class PublicacionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'publicaciones/editar_publicacion.html'
    success_url = reverse_lazy('publicaciones:inicio')
    success_message = '¡La publicación se actualizó correctamente!'

    # EL MISMO GUARDIA PARA LA EDICIÓN
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, 'es_empleado', False) and not getattr(request.user, 'es_empresa', False):
            messages.error(request, "No tienes un perfil de trabajo válido para editar.")
            return redirect('publicaciones:crear_perfil_trabajo')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if getattr(self.request.user, 'es_empleado', False):
            return queryset.filter(empleado=self.request.user.empleado)
        elif getattr(self.request.user, 'es_empresa', False):
            return queryset.filter(empresa=self.request.user.empresa)
        return queryset.none()


#Vista basada en clase para Eliminar una publicacion (Update)
class PublicacionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Publicacion
    template_name = 'publicaciones/confirmar_eliminar.html'
    success_url = reverse_lazy('publicaciones:inicio')
    success_message = 'La publicación fue eliminada con éxito.'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.user.es_empleado:
            return queryset.filter(empleado=self.request.user.empleado)
        elif self.request.user.es_empresa:
            return queryset.filter(empresa=self.request.user.empresa)
            
        return queryset.none()


def CrearPerfilTrabajoView(request):
    return render(request, 'publicaciones/crear_perfil_trabajo.html')

class ReporteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ReportePublicacion
    fields = ['motivo']
    template_name = 'publicaciones/reporte_form.html'
    success_url = reverse_lazy('publicaciones:lista') # URL a donde redirige tras reportar con éxito

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='visores').exists() or user.is_staff

    def form_valid(self, form):
        # 1. Capturamos la publicación mediante el PK que viene en la URL
        publicacion_pk = self.kwargs.get('pk')
        form.instance.publicacion = get_object_or_404(Publicacion, pk=publicacion_pk)
        
        # 2. Asignamos automáticamente al usuario logueado como autor del reporte
        form.instance.usuario = self.request.user
        
        return super().form_valid(form)


class ReporteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ReportePublicacion
    fields = ['estado'] # Permitimos cambiar el estado (ej. de 'pendiente' a 'resuelto')
    template_name = 'publicaciones/reporte_update.html'
    success_url = reverse_lazy('publicaciones:lista') # O la ruta de tu panel de moderación

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='visores').exists() or user.is_staff