from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.urls import re_path
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve
from django.conf.urls.i18n import i18n_patterns
from blog import views  # Importa las vistas desde tu app blog

handler404 = 'blog.views.custom_404'

urlpatterns = [
    path('adminmarmorten/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n'))
]

# URLs internacionalizadas
urlpatterns += i18n_patterns(
    path('', views.inicio, name='inicio'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('nuestro-equipo/', views.nuestro_equipo, name='nuestro_equipo'),
    path('buscar/', views.buscar_posts, name='buscar_posts'),
    prefix_default_language=True,
)

# Configuración para archivos estáticos y media
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]