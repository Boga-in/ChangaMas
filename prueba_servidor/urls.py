from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # RUTA PARA LA APP CORE:
    path('', include('core.urls')), 
    
    # RUTA PARA PUBLICACIONES:
    path('publicaciones/', include('publicaciones.urls')),
]