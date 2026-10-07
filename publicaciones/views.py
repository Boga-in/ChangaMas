from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import request
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,TemplateView

from .forms import PublicacionForm
from .models import Publicacion
from django.contrib.auth.decorators import login_required

#Vista basada en clase para crear una publicacion (Create)

class InicioView(ListView):
    model = Publicacion
    template_name = 'publicaciones/inicio.html'
    context_object_name = 'publicaciones'
    paginate_by = 10

    def get_queryset(self):
        # 1. Obtenemos la consulta base (todos los empleados)
        queryset = super().get_queryset()
        
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
class PublicacionListView(ListView):
    model = Publicacion
    template_name = 'publicaciones/listar_publicaciones.html'
    context_object_name = 'publicaciones'
    paginate_by = 10

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
class PublicacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'publicaciones/editar_publicacion.html'
    success_url = reverse_lazy('publicaciones:inicio')
    success_message = '¡La publicación se actualizó correctamente!'

    def test_func(self):
        publicacion = self.get_object()
        return self.request.user == publicacion.self


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