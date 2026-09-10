from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from publicaciones.views import crear_publicacion, inicio, listar_publicaciones

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('admin/login', crear_publicacion, name='admin'),
    path('crear/', crear_publicacion, name='crear_publicacion'),
    path('listar/', listar_publicaciones, name='listar_publicaciones'),
    path('publicaciones/', include('publicaciones.urls')),
    path('', inicio, name='inicio'),
]

# Esta inyección permite al servidor local entregar las imágenes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
