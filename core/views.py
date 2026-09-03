from django.shortcuts import render

def inicio(request):
    # Cambiamos la ruta de la plantilla a la carpeta core
    return render(request, 'core/inicio.html')