from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve
from django.conf.urls.i18n import i18n_patterns
handler404 = 'blog.views.custom_404'


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('nuestro-equipo/', views.nuestro_equipo, name='nuestro_equipo'),
    path('buscar/', views.buscar_posts, name='buscar_posts'),
    path('i18n/', include('django.conf.urls.i18n')),
]

handler404 = 'blog.views.custom_404'

# Configuración para desarrollo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Configuración para producción (DEBUG=False)
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
urlpatterns += i18n_patterns(
    path('', include('blog.urls')),  # Tus URLs de la aplicación blog
    prefix_default_language=False,
)