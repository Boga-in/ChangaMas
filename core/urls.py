from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from publicaciones.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('publicaciones/', include('publicaciones.urls')),
    path('usuarios/', include('usuarios.urls')),
]

# Esta inyección permite al servidor local entregar las imágenes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
