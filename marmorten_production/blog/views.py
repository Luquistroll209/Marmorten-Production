from django.shortcuts import render
from .models import Post

def inicio(request):
    posts = Post.objects.all().order_by('-fecha_publicacion')
    return render(request, 'blog/index.html', {'posts': posts})

