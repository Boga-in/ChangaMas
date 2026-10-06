from django.shortcuts import render, redirect  # <-- Agregamos redirect
from django.http import HttpResponse
from django.contrib import messages  # <-- Importamos el sistema de mensajes
from .forms import PublicacionForm
from .models import Publicacion
from django.contrib.auth.decorators import login_required

@login_required
def crear_publicacion(request):
    #esto es para que si el usuario no esta logueado no pueda crear publicaciones
    #if not request.user.is_authenticated:
    #   return redirect('login')
    #Si el usuario da al boton guardar
    if request.method == 'POST':
        formulario = PublicacionForm(request.POST, request.FILES)
    
        if formulario.is_valid():
            # Como el formulario ya tiene todo, simplemente lo guardamos
            formulario.save()
            messages.success(request, '¡La publicación se creó correctamente!')
            return redirect('inicio')
    elif request.method == 'GET':
        formulario = PublicacionForm()

    return render(request, 'publicaciones/crear_publicacion.html', {'formulario': formulario})

def listar_publicaciones(request):
    # Traemos TODOS los registros de la tabla Publicacion
    publicaciones_guardadas = Publicacion.objects.all()
    # Seguridad básica: bloqueamos a quienes no tengan la sesión iniciada o no sean admin_general
    if not request.user.is_authenticated or not request.user.is_staff:
        return render(request, 'publicaciones/muro.html', {'publicaciones': publicaciones_guardadas})    
    
    # Enviamos la lista a una nueva plantilla HTML
    return render(request, 'publicaciones/lista_publicaciones.html', {'publicaciones': publicaciones_guardadas})

def inicio(request):
    # Traemos todas las publicaciones de la base de datos. 
    # .order_by('-id') las ordena de la más nueva a la más vieja)
    publicaciones_recientes = Publicacion.objects.all().order_by('-id')
    termino_busqueda = request.GET.get('q')
        
    if termino_busqueda:
            # __icontains busca coincidencias parciales sin importar mayúsculas/minúsculas
            publicaciones_recientes = publicaciones_recientes.filter(titulo__icontains=termino_busqueda)
        
    contexto = {
        'publicaciones': publicaciones_recientes,
        'busqueda': termino_busqueda
    }

    # 5. Envías el contexto al template
    return render(request, 'publicaciones/inicio.html', contexto)

def crear_perfil_trabajo(request):
    # Aquí iría la lógica para crear un perfil de trabajo
    return render(request, 'publicaciones/crear_perfil_trabajo.html')