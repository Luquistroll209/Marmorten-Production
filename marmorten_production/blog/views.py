from django.shortcuts import render, get_object_or_404
from .models import Post, CarruselPost

def inicio(request):
    carrusel_items = CarruselPost.objects.filter(activo=True).select_related('post').order_by('orden')
    posts_destacados = Post.objects.filter(destacado=True).exclude(imagen='').order_by('-fecha_publicacion')[:4]
    ultimos_posts = Post.objects.all().order_by('-fecha_publicacion')[:6]
    
    context = {
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