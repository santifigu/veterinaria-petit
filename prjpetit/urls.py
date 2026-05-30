from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Core
    path('contacto/', include('contacto.urls')), # Contacto
    path('servicios/', include('servicios.urls')), # Servicios
    path('tienda/', include('tienda.urls')), # Tienda
    path('domicilio/', include('domicilio.urls')), # Domicilio
    path('turnos/', include('turnos.urls')), # Turnos
    path('blog/', include('blog.urls')), # Blog
    path('mascota/', include('mascota.urls')), # Mascota
    path('veterinario/', include('veterinario.urls')), # Veterinarios
    path('tutor/', include('tutor.urls')), # Tutor
    path('carro/', include('carro.urls')), # Carro - Para usar las funcionalidades del carro
    path('autenticacion/', include('autenticacion.urls')), # Para usar las funcionalidades de autenticación de Django
    path('pedidos/', include('pedidos.urls')),
]

handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler403 = 'core.views.error_403'

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    