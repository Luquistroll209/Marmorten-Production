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

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    biografia = models.TextField()
    foto = models.ImageField(upload_to='equipo/')
    orden = models.PositiveIntegerField(default=0)
    redes_sociales = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Miembros del equipo"

    def __str__(self):
        return self.nombre

class ConfiguracionSitio(models.Model):
    # Información Básica
    titulo_sitio = models.CharField(max_length=200, default="Marmoten Production")
    logo = models.ImageField(upload_to='config/', blank=True, null=True)
    email_contacto = models.EmailField(default='contacto@marmoten.com')
    telefono_contacto = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    
    # Sobre Nosotros - Contenido
    sobre_nosotros = models.TextField(blank=True)
    mision = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    
    # Sobre Nosotros - Imágenes (Nuevos campos)
    banner_sobre_nosotros = models.ImageField(
        upload_to='config/sobre_nosotros/',
        blank=True,
        null=True,
        help_text="Banner para la página 'Sobre Nosotros' (1920x500px recomendado)"
    )
    imagen_sobre_nosotros = models.ImageField(
        upload_to='config/sobre_nosotros/',
        blank=True,
        null=True,
        help_text="Imagen descriptiva para 'Sobre Nosotros' (800x600px recomendado)"
    )
    icono_mision = models.ImageField(
        upload_to='config/iconos/',
        blank=True,
        null=True,
        help_text="Icono para la sección Misión (200x200px recomendado)"
    )
    icono_vision = models.ImageField(
        upload_to='config/iconos/',
        blank=True,
        null=True,
        help_text="Icono para la sección Visión (200x200px recomendado)"
    )
    
    # Redes Sociales
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Configuraciones del Sitio"

    def __str__(self):
        return "Configuración del Sitio"

class ImagenGaleriaSobreNosotros(models.Model):
    configuracion = models.ForeignKey(
        ConfiguracionSitio, 
        related_name='galeria_sobre_nosotros', 
        on_delete=models.CASCADE
    )
    imagen = models.ImageField(upload_to='galeria_sobre_nosotros/')
    titulo = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Galería Sobre Nosotros"

    def __str__(self):
        return self.titulo or f"Imagen {self.id}"
    
from django.db import models

class SeccionPersonalizable(models.Model):
    TIPO_CONTENIDO = [
        ('TEXTO', 'Texto'),
        ('IMAGEN', 'Imagen'),
        ('CAROUSEL', 'Carrusel'),
        ('ENLACE', 'Enlace'),
    ]
    
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CONTENIDO)
    contenido_texto = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='secciones/', blank=True, null=True)
    enlace_url = models.URLField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    formato_texto = models.CharField(max_length=20, choices=[
        ('NORMAL', 'Normal'), 
        ('NEGRITA', 'Negrita'),
        ('CURSIVA', 'Cursiva')
    ], default='NORMAL')
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Secciones editables"

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"

class ImagenCarrusel(models.Model):
    seccion = models.ForeignKey(
        SeccionPersonalizable, 
        on_delete=models.CASCADE, 
        related_name='imagenes_carrusel'  # ¡Este nombre debe coincidir con el usado en el template!
    )
    imagen = models.ImageField(upload_to='carrusel/')
    titulo = models.CharField(max_length=100, blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']