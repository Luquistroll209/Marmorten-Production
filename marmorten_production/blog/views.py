from django.db.models import Q  
from django.shortcuts import render, get_object_or_404, redirect 
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, CarruselPost, Equipo, ConfiguracionSitio, SeccionSobreNosotros
from django.http import Http404
from django.contrib import messages

def custom_404(request, exception):
    config = ConfiguracionSitio.objects.first()
    context = {
        'config': config,
    }
    return render(request, 'blog/404.html', context, status=404)

def inicio(request):
    config = ConfiguracionSitio.objects.first()
    carrusel_items = CarruselPost.objects.filter(activo=True).select_related('post').order_by('orden')
    posts_destacados = Post.objects.filter(destacado=True).exclude(imagen='').order_by('-fecha_publicacion')#[:4]
    ultimos_posts = Post.objects.all().order_by('-fecha_publicacion')#[:6]
    
    print("Config:", config)
    print("Carrusel items:", carrusel_items)
    print("Posts destacados:", posts_destacados)
    print("Últimos posts:", ultimos_posts)
    
    context = {
        'config': config,
        'carrusel_items': carrusel_items,
        'posts_destacados': posts_destacados,
        'ultimos_posts': ultimos_posts
    }
    return render(request, 'blog/index.html', context)

def detalle_post(request, post_id):
    config = ConfiguracionSitio.objects.first()
    post = get_object_or_404(Post, pk=post_id)
    galeria = post.galeria.all().order_by('orden')
    relacionados = Post.objects.exclude(pk=post_id).exclude(imagen='').order_by('-fecha_publicacion')[:3]
    
    context = {
        'config': config,
        'post': post,
        'galeria': galeria,
        'relacionados': relacionados
    }
    return render(request, 'blog/detalle_post.html', context)

def sobre_nosotros(request):
    portada = SeccionSobreNosotros.objects.filter(tipo='PORTADA').first()
    secciones = SeccionSobreNosotros.objects.exclude(tipo='PORTADA').order_by('orden')
    config = ConfiguracionSitio.objects.first()
    
    context = {
        'portada': portada,
        'secciones': secciones,
        'config': config
    }
    return render(request, 'blog/sobre_nosotros.html', context)

def nuestro_equipo(request):
    config = ConfiguracionSitio.objects.first()
    equipo = Equipo.objects.all().order_by('orden')
    posts_destacados = Post.objects.filter(
        destacado=True
    ).exclude(
        imagen=''
    ).order_by(
        '-fecha_publicacion'
    )#[:3] 
    
    context = {
        'config': config,
        'equipo': equipo,
        'posts_destacados': posts_destacados,
    }
    
    return render(request, 'blog/nuestro_equipo.html', context)


def sobre_nosotros(request):
    portada = SeccionSobreNosotros.objects.filter(tipo='PORTADA').first()
    secciones = SeccionSobreNosotros.objects.exclude(tipo='PORTADA').order_by('orden')
    config = ConfiguracionSitio.objects.first()
    
    context = {
        'portada': portada,
        'secciones': secciones,
        'config': config
    }
    return render(request, 'blog/sobre_nosotros.html', context)

def contacto(request):
    config = ConfiguracionSitio.objects.first() 
    context = {
        'config': config,  
    }
    return render(request, 'blog/contacto.html', context)


def buscar_posts(request):
    query = request.GET.get('q', '')
    config = ConfiguracionSitio.objects.first()
    
    if query:
        resultados = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(resumen__icontains=query)
        ).order_by('-fecha_publicacion')
    else:
        resultados = Post.objects.none()
    
    context = {
        'resultados': resultados,
        'query': query,
        'config': config
    }
    return render(request, 'blog/resultados_busqueda.html', context)

def contacto(request):
    config = ConfiguracionSitio.objects.first()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        asunto = request.POST.get('asunto', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        
        # Inicializa la lista de errores
        errores = []
        
        # Validación básica
        if not nombre:
            errores.append('El nombre es obligatorio')
        if not email:
            errores.append('El email es obligatorio')
        elif '@' not in email:
            errores.append('El email no es válido')
        if not mensaje:
            errores.append('El mensaje es obligatorio')
        
        if not errores:  # Si no hay errores
            # Guardar en base de datos (opcional)
            from .models import MensajeContacto  # Asegúrate de tener este modelo
            MensajeContacto.objects.create(
                nombre=nombre,
                email=email,
                asunto=asunto,
                mensaje=mensaje
            )
            
            messages.success(request, '¡Mensaje recibido! Nos pondremos en contacto contigo pronto.')
            return redirect('contacto')
        else:
            for error in errores:
                messages.error(request, error)
    
    context = {
        'config': config,
    }
    return render(request, 'blog/contacto.html', context)