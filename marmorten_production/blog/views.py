from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, CarruselPost, Equipo, ConfiguracionSitio, SeccionSobreNosotros
from .forms import ContactoForm  # Crearás este formulario después

# Vistas existentes (inicio, detalle_post) se mantienen igual
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
    post = get_object_or_404(Post, pk=post_id)
    galeria = post.galeria.all().order_by('orden')
    relacionados = Post.objects.exclude(pk=post_id).exclude(imagen='').order_by('-fecha_publicacion')[:3]
    
    context = {
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

def contacto(request):
    config = ConfiguracionSitio.objects.first()
    mensaje_enviado = False
    
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Enviar correo
            send_mail(
                f"Mensaje de contacto de {form.cleaned_data['nombre']}",
                form.cleaned_data['mensaje'],
                form.cleaned_data['email'],
                [config.email_contacto],
                fail_silently=False,
            )
            mensaje_enviado = True
    else:
        form = ContactoForm()
    
    context = {
        'config': config,
        'form': form,
        'mensaje_enviado': mensaje_enviado,
        'carrusel_items': CarruselPost.objects.filter(activo=True).select_related('post').order_by('orden')[:3]
    }
    return render(request, 'blog/contacto.html', context)

def nuestro_equipo(request):
    equipo = Equipo.objects.all().order_by('orden')
    config = ConfiguracionSitio.objects.first()
    
    context = {
        'equipo': equipo,
        'config': config,
        'posts_destacados': Post.objects.filter(destacado=True).exclude(imagen='').order_by('-fecha_publicacion')[:3]
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
    config = ConfiguracionSitio.objects.first()  #  Importante
    context = {
        'config': config,  #  Pasa la configuración
    }
    return render(request, 'blog/contacto.html', context)

def nuestro_equipo(request):
    config = ConfiguracionSitio.objects.first()  #  Importante
    secciones = SeccionSobreNosotros.objects.all().order_by('orden')

    config = ConfiguracionSitio.objects.first()  #  Importante
    context = {
        'config': config,  #  Pasa la configuración
        'secciones': secciones
    }
    return render(request,  'blog/nuestro_equipo.html', context)