from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True, help_text="Breve resumen para mostrar en las tarjetas")
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    destacado = models.BooleanField(default=False)
    mostrar_en_carrusel = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-fecha_publicacion']
    def tiene_imagen(self):
        return bool(self.imagen)
    
    def __str__(self):
        return self.title

class CarruselPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"Carrusel: {self.titulo or self.post.title}"

class GaleriaImagenes(models.Model):
    post = models.ForeignKey(Post, related_name='galeria', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='galeria/')
    titulo = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return self.titulo or f"Imagen {self.id}"