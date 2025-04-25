from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    destacado = models.BooleanField(default=False, help_text="Marcar para mostrar en el carrusel principal")
    orden_carrusel = models.PositiveIntegerField(default=0, help_text="Orden de aparición en el carrusel (mayor número = más adelante)")
    mostrar_en_encabezado = models.BooleanField(default=False, help_text="Mostrar en el carrusel del encabezado")
    
    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
    
    def __str__(self):
        return self.title

class CarruselEncabezado(models.Model):
    titulo = models.CharField(max_length=200, blank=True)
    subtitulo = models.CharField(max_length=300, blank=True)
    activo = models.BooleanField(default=True)
    velocidad_transicion = models.PositiveIntegerField(
        default=5000,
        help_text="Velocidad de transición entre slides en milisegundos"
    )
    efecto_transicion = models.CharField(
        max_length=20,
        choices=[
            ('desvanecimiento', 'Desvanecimiento'),
            ('deslizamiento', 'Deslizamiento'),
        ],
        default='desvanecimiento'
    )
    posts = models.ManyToManyField(
        Post,
        blank=True,
        limit_choices_to={'mostrar_en_encabezado': True},
        help_text="Posts para mostrar en el carrusel"
    )
    
    def __str__(self):
        return f"Carrusel: {self.titulo or 'Sin título'}"

class ImagenCarrusel(models.Model):
    titulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='carrusel/')
    enlace = models.URLField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    carrusel = models.ForeignKey(CarruselEncabezado, related_name='imagenes_personalizadas', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Imagen de Carrusel'
        verbose_name_plural = 'Imágenes de Carrusel'
    
    def __str__(self):
        return self.titulo or f"Imagen {self.id}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author}"