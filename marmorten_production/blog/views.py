from django.shortcuts import render
from .models import Post, CarruselEncabezado

def inicio(request):
    posts = Post.objects.all().order_by('-fecha_publicacion')
    carrusel_activo = CarruselEncabezado.objects.filter(activo=True).first()
    
    context = {
        'posts': posts,
        'carrusel': carrusel_activo,
        'posts_destacados': Post.objects.filter(destacado=True).order_by('-orden_carrusel')[:5]
    }
    return render(request, 'blog/index.html', context)