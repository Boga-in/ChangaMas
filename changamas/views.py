from django.shortcuts import render, redirect  # <-- Agregamos redirect
from django.http import HttpResponse
from django.contrib import messages  # <-- Importamos el sistema de mensajes
from .forms import PublicacionForm
from .models import Publicacion

# 1. Creamos la nueva vista para la página de inicio
def inicio(request):
    return render(request, 'changamas/inicio.html')

# 2. Modificamos tu vista actual
def crear_publicacion(request):
    #esto es para que si el usuario no esta logueado no pueda crear publicaciones
    if not request.user.is_authenticated:
        return HttpResponse("Por favor, inicia sesión...")
    #Si el usuario da al boton guardar
    if request.method == 'POST':
        formulario = PublicacionForm(request.POST)
        
        if formulario.is_valid():
            # Guardamos la publicación, pero no la confirmamos todavía
            publicacion = formulario.save(commit=False)
            # Asignamos el autor de la publicación al usuario que está haciendo la solicitud (Es la manera en que se me ocurrio seguro existe una mejor)
            publicacion.autor = request.user
            publicacion.save()
            
            # Preparamos el cartel de éxito
            messages.success(request, '¡La publicación se creó correctamente!')
            # Y enviamos al usuario de vuelta a la página de inicio
            return redirect('inicio')
    
    else:
        formulario = PublicacionForm()

    return render(request, 'changamas/crear_publicacion.html', {'formulario': formulario})

def listar_publicaciones(request):
    # Seguridad básica: bloqueamos a quienes no tengan la sesión iniciada o no sean admin_general
    if not request.user.is_authenticated or not request.user.es_admin_general:
        return HttpResponse("Acceso denegado. Solo los administradores generales pueden ver esta página.")
    
    # Traemos TODOS los registros de la tabla Publicacion
    publicaciones_guardadas = Publicacion.objects.all()
    
    # Enviamos la lista a una nueva plantilla HTML
    return render(request, 'changamas/lista_publicaciones.html', {'publicaciones': publicaciones_guardadas})