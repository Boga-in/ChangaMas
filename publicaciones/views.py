from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView

from .forms import PublicacionForm
from .models import Publicacion

#Vista basada en clase para crear una publicacion (Create)
class PublicacionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'publicaciones/crear_publicacion.html'
    success_url = reverse_lazy('inicio')
    success_message = '¡La publicación se creó correctamente!'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
#Vista basada en clase para ver una publicacion (Read)
class PublicacionDetailView(DetailView):
    model = Publicacion
    template_name = 'publicaciones/detalle_publicacion.html'
    context_object_name = 'publicacion'

#Vista basada en clase para Listar las publicaciones
class PublicacionListView(ListView):
    model = Publicacion
    template_name = 'publicaciones/lista_publicaciones.html'
    context_object_name = 'publicaciones'
    paginate_by = 10

#Vista basada en clase para Editar una publicacion (Update)
class PublicacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'publicaciones/editar_publicacion.html'
    success_url = reverse_lazy('inicio')
    success_message = '¡La publicación se actualizó correctamente!'

    def test_func(self):
        publicacion = self.get_object()
        return self.request.user == publicacion.autor


#Vista basada en clase para Eliminar una publicacion (Update)
class PublicacionDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Publicacion
    template_name = 'publicaciones/confirmar_eliminar.html'
    success_url = reverse_lazy('inicio')
    success_message = 'La publicación fue eliminada con éxito.'

    def test_func(self):
        publicacion = self.get_object()
        return self.request.user == publicacion.autor