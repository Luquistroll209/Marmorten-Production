from django.db.models import Q  
from django.shortcuts import render, get_object_or_404, redirect 
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, CarruselPost, Equipo, ConfiguracionSitio, SeccionSobreNosotros
from django.http import Http404
from django.contrib import messages
from django.utils.translation import get_language
from urllib.parse import urlparse, urlunparse


def get_config():
    """Función helper para obtener la configuración del sitio una sola vez por request"""
    config = ConfiguracionSitio.objects.first()
    if not config:
        return None
        
    # Añade la descripción según el idioma
    from django.utils.translation import get_language
    if get_language() == 'en' and config.descripcion_en:
        config.descripcion_actual = config.descripcion_en
    else:
        config.descripcion_actual = config.descripcion
        
    return config

def custom_404(request, exception):
    return render(request, 'blog/404.html', {'config': get_config()}, status=404)

def inicio(request):
    context = {
        'config': get_config(),
        'carrusel_items': CarruselPost.objects.filter(activo=True).select_related('post').order_by('orden'),
        'posts_destacados': Post.objects.filter(destacado=True).exclude(imagen='').order_by('-fecha_publicacion'),
        'ultimos_posts': Post.objects.all().order_by('-fecha_publicacion')
    }
    return render(request, 'blog/index.html', context)

def detalle_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'config': get_config(),
        'post': post,
        'galeria': post.galeria.all().order_by('orden'),
        'relacionados': Post.objects.exclude(pk=post_id).exclude(imagen='').order_by('-fecha_publicacion')[:3]
    }
    return render(request, 'blog/detalle_post.html', context)

def sobre_nosotros(request):
    context = {
        'portada': SeccionSobreNosotros.objects.filter(tipo='PORTADA').first(),
        'secciones': SeccionSobreNosotros.objects.exclude(tipo='PORTADA')
                              .order_by('orden')
                              .prefetch_related('imagenes_del_carrusel'),
        'config': get_config()
    }
    return render(request, 'blog/sobre_nosotros.html', context)

def nuestro_equipo(request):
    context = {
        'config': get_config(),
        'equipo': Equipo.objects.all().order_by('orden'),
        'posts_destacados': Post.objects.filter(destacado=True).exclude(imagen='').order_by('-fecha_publicacion')
    }
    return render(request, 'blog/nuestro_equipo.html', context)

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        asunto = request.POST.get('asunto', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        
        errores = []
        if not nombre:
            errores.append('El nombre es obligatorio')
        if not email:
            errores.append('El email es obligatorio')
        elif '@' not in email:
            errores.append('El email no es válido')
        if not mensaje:
            errores.append('El mensaje es obligatorio')
        
        if not errores:
            from .models import MensajeContacto
            MensajeContacto.objects.create(
                nombre=nombre,
                email=email,
                asunto=asunto,
                mensaje=mensaje
            )
            messages.success(request, '¡Mensaje recibido! Nos pondremos en contacto contigo pronto.')
            return redirect('contacto')
        
        for error in errores:
            messages.error(request, error)
    
    return render(request, 'blog/contacto.html', {'config': get_config()})

def buscar_posts(request):
    query = request.GET.get('q', '')
    resultados = Post.objects.none()
    
    if query:
        resultados = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(resumen__icontains=query)
        ).order_by('-fecha_publicacion')
    
    context = {
        'resultados': resultados,
        'query': query,
        'config': get_config()
    }
    return render(request, 'blog/resultados_busqueda.html', context)

def your_view(request):
    # Obtener la URL actual
    full_path = request.get_full_path()
    
    # Parsear la URL
    parsed_url = urlparse(full_path)
    path_parts = parsed_url.path.strip('/').split('/')
    
    # Eliminar el código de idioma si está como primer segmento
    current_lang = get_language()  # por ejemplo 'en' o 'es'
    if path_parts and path_parts[0] == current_lang:
        path_parts.pop(0)

    # Reconstruir la ruta
    new_path = '/' + '/'.join(path_parts) if path_parts else '/'

    # Volver a armar la URL completa
    redirect_to = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        new_path,
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))

    return render(request, 'tu_template.html', {'redirect_to': redirect_to})