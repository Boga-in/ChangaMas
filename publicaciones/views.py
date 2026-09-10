from django.shortcuts import render, redirect  # <-- Agregamos redirect
from django.http import HttpResponse
from django.contrib import messages  # <-- Importamos el sistema de mensajes
from .forms import PublicacionForm
from .models import Publicacion


def crear_publicacion(request):
    #esto es para que si el usuario no esta logueado no pueda crear publicaciones
    if not request.user.is_authenticated:
        return redirect('admin:index')  # Redirige a la página de inicio de sesión si el usuario no está autenticado
    #Si el usuario da al boton guardar
    if request.method == 'POST':
        formulario = PublicacionForm(request.POST, request.FILES)
        
        if formulario.is_valid():
            # Guardamos la publicación, pero no la confirmamos todavía
            publicacion = formulario.save(commit=False)
            # Asignamos el autor de la publicación al usuario que está haciendo la solicitud (Es la manera en que se me ocurrio seguro existe una mejor)
            publicacion.autor = request.user
            publicacion.foto_perfil = request.FILES.get('foto_perfil')  # <-- Guardamos la foto de perfil
            publicacion.save()
            
            # Preparamos el cartel de éxito
            messages.success(request, '¡La publicación se creó correctamente!')
            # Y enviamos al usuario de vuelta a la página de inicio
            return redirect('inicio')
    
    elif request.method == 'GET':
        formulario = PublicacionForm()

    return render(request, 'publicaciones/crear_publicacion.html', {'formulario': formulario})

def listar_publicaciones(request):
    # Traemos TODOS los registros de la tabla Publicacion
    publicaciones_guardadas = Publicacion.objects.all()
    # Seguridad básica: bloqueamos a quienes no tengan la sesión iniciada o no sean admin_general
    if not request.user.is_authenticated or not request.user.es_admin_general:
        return render(request, 'publicaciones/muro.html', {'publicaciones': publicaciones_guardadas})    
    
    # Enviamos la lista a una nueva plantilla HTML
    return render(request, 'publicaciones/lista_publicaciones.html', {'publicaciones': publicaciones_guardadas})
    