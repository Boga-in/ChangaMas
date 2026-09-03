from django.shortcuts import render
from publicaciones.models import Publicacion

def inicio(request):
    # Traemos todas las publicaciones de la base de datos. 
    # .order_by('-id') las ordena de la más nueva a la más vieja)
    publicaciones_recientes = Publicacion.objects.all().order_by('-id')
    
    # Armamos el contexto para pasarlo al HTML
    contexto = {
        'publicaciones': publicaciones_recientes
    }
    
    # Renderizamos la plantilla pasándole el contexto
    return render(request, 'core/inicio.html', contexto)