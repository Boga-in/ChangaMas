from django.shortcuts import render, redirect  # <-- Agregamos redirect
from django.http import HttpResponse
from django.contrib import messages  # <-- Importamos el sistema de mensajes
from .forms import PublicacionEmpleadoForm, PublicacionEmpresaForm
from .models import Publicacion
from django.contrib.auth.decorators import login_required

@login_required
def crear_publicacion(request):
    #esto es para que si el usuario no esta logueado no pueda crear publicaciones
    #if not request.user.is_authenticated:
    #   return redirect('login')
    #Si el usuario da al boton guardar
    if request.method == 'POST':
        # Si el usuario es un empleado, usamos el formulario de empleado sino el de empresa
        if request.user.es_empleado:
            formulario = PublicacionEmpleadoForm(request.POST, request.FILES, usuario_actual=request.user)
        
            if formulario.is_valid():
                # Como el formulario ya tiene todo, simplemente lo guardamos
                formulario.save()
                messages.success(request, '¡La publicación se creó correctamente!')
                return redirect('inicio')
        elif request.user.es_empresa:
                formulario = PublicacionEmpresaForm(request.POST, request.FILES, usuario_actual=request.user)
                
                if formulario.is_valid():
                    # Como el formulario ya tiene todo, simplemente lo guardamos
                    formulario.save()
                    messages.success(request, '¡La publicación se creó correctamente!')
                    return redirect('inicio')
    elif request.method == 'GET':
        if request.user.es_empleado:
            formulario = PublicacionEmpleadoForm(usuario_actual=request.user)
        elif request.user.es_empresa:
            formulario = PublicacionEmpresaForm(usuario_actual=request.user)

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
    
    # Armamos el contexto para pasarlo al HTML
    contexto = {
        'publicaciones': publicaciones_recientes
    }
    
    # Renderizamos la plantilla pasándole el contexto
    return render(request, 'publicaciones/inicio.html', contexto)