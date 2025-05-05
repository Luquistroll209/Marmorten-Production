from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.urls import re_path
from django.contrib.staticfiles.views import serve
from django.views.static import serve as static_serve

handler404 = 'blog.views.custom_404'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('nuestro-equipo/', views.nuestro_equipo, name='nuestro_equipo'),
    path('buscar/', views.buscar_posts, name='buscar_posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]