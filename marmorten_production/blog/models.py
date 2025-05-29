from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language  # Add this line
from ckeditor.fields import RichTextField

class TipoTrabajo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre (Español)")
    nombre_en = models.CharField(max_length=100, verbose_name="Nombre (Inglés)", blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    descripcion_en = models.TextField(blank=True, null=True, verbose_name="Descripción (Inglés)")
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Tipos de Trabajo"
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_nombre_translated(self):
        lang = get_language()
        if lang == 'en' and self.nombre_en:
            return self.nombre_en
        return self.nombre


class Post(models.Model):
    
    title = models.CharField(_('Título'), max_length=200)
    content = RichTextField(_('Contenido'), blank=True, null=True)
    resumen = RichTextField(blank=True, null=True, help_text="Breve resumen para mostrar en las tarjetas")
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    destacado = models.BooleanField(default=False)
    mostrar_en_carrusel = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    tipo_trabajo = models.ForeignKey(
        TipoTrabajo, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Tipo de trabajo'
    )


    class Meta:
        ordering = ['-fecha_publicacion']
    
    def tiene_imagen(self):
        return bool(self.imagen)
    
    def __str__(self):
        return self.title
    

    TIPO_ENLACE_CHOICES = [
        ('YOUTUBE', 'YouTube'),
        ('INSTAGRAM', 'Instagram'),
        ('FACEBOOK', 'Facebook'),
        ('TWITTER', 'Twitter/X'),
        ('OTRO', 'Otro'),
    ]
    
class EnlaceExterno(models.Model):
    TIPO_ENLACE_CHOICES = [
        ('YOUTUBE', 'YouTube'),
        ('INSTAGRAM', 'Instagram'),
        ('FACEBOOK', 'Facebook'),
        ('TWITTER', 'Twitter/X'),
        ('OTRO', 'Otro'),
    ]
    
    post = models.ForeignKey(
        Post, 
        related_name='enlaces_externos', 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    equipo = models.ForeignKey(
        'Equipo',  
        related_name='enlaces_externos',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    url = models.URLField()
    tipo = models.CharField(max_length=10, choices=TIPO_ENLACE_CHOICES)
    mostrar = models.BooleanField(default=True)
    titulo = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo or self.url}"
    
    def get_icon_class(self):
        iconos = {
            'YOUTUBE': 'fab fa-youtube',
            'INSTAGRAM': 'fab fa-instagram',
            'FACEBOOK': 'fab fa-facebook-f',
            'TWITTER': 'fab fa-twitter',
            'OTRO': 'fas fa-external-link-alt',
        }
        return iconos.get(self.tipo, 'fas fa-link')

    def clean(self):
        if not self.post and not self.equipo:
            raise ValidationError("El enlace debe estar asociado a un Post o a un Miembro del Equipo")
        if self.post and self.equipo:
            raise ValidationError("El enlace solo puede estar asociado a un Post o a un Miembro del Equipo, no a ambos")
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo or self.url}"
    
    def get_icon_class(self):
        iconos = {
            'YOUTUBE': 'fab fa-youtube',
            'INSTAGRAM': 'fab fa-instagram',
            'FACEBOOK': 'fab fa-facebook-f',
            'TWITTER': 'fab fa-twitter',
            'OTRO': 'fas fa-external-link-alt',
        }
        return iconos.get(self.tipo, 'fas fa-link')

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

from django.db import models

from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    biografia = RichTextField(blank=True)
    foto = models.ImageField(upload_to='equipo/')
    orden = models.PositiveIntegerField(default=0)
    redes_sociales = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Miembros del equipo"

    def __str__(self):
        return f"{self.nombre} - {self.puesto}"

    # Añade esta propiedad para acceder a los enlaces fácilmente
    @property
    def enlaces_externos(self):
        return self.enlaces_externos_equipo.all()

class ConfiguracionSitio(models.Model):
    # Información Básica
    titulo_sitio = models.CharField(max_length=200, default="Marmoten Production")
    logo = models.ImageField(upload_to='config/', blank=True, null=True)
    email_contacto = models.EmailField(default='contacto@marmoten.com')
    direccion = models.TextField(blank=True)
    descripcion = RichTextField(blank=True)
    descripcion_en = RichTextField(blank=True, null=True, verbose_name="Descripción (Inglés)")
    
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
    imb_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Configuraciones del Sitio"

    def __str__(self):
        return "Configuración del Sitio"
class TelefonoContacto(models.Model):
    configuracion = models.ForeignKey(
        ConfiguracionSitio, 
        related_name='telefonos', 
        on_delete=models.CASCADE
    )
    numero = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=100, blank=True, help_text="Ej: Oficina, Móvil, WhatsApp")
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Teléfonos de Contacto"
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

class SeccionSobreNosotros(models.Model):
    TIPO_SECCION = [
        ('PORTADA', 'Portada (solo una)'),
        ('TEXTO', 'Texto'),
        ('IMAGEN', 'Imagen'),
        ('CAROUSEL', 'Carrusel de imágenes'),
        ('REDES', 'Enlaces/Redes Sociales'),
    ]
    
    POSICION_CARRUSEL = [
        ('DERECHA', 'Derecha'),
        ('IZQUIERDA', 'Izquierda'),
        ('NINGUNA', 'Sin carrusel'),
    ]
    
    titulo = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_SECCION)
    contenido_texto = RichTextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='sobre_nosotros/secciones/', blank=True, null=True)
    carrusel_asociado = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'tipo': 'CAROUSEL'},
        help_text="Selecciona un carrusel para mostrar con esta sección"
    )
    posicion_carrusel = models.CharField(
        max_length=10,
        choices=POSICION_CARRUSEL,
        default='NINGUNA',
        help_text="Posición del carrusel respecto al texto"
    )
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Secciones Sobre Nosotros"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.tipo == 'PORTADA' and SeccionSobreNosotros.objects.filter(tipo='PORTADA').exclude(id=self.id).exists():
            raise ValidationError('Solo puede haber una sección de tipo Portada')
        if self.tipo == 'CAROUSEL' and self.carrusel_asociado:
            raise ValidationError('Un carrusel no puede tener otro carrusel asociado')
        if self.posicion_carrusel != 'NINGUNA' and not self.carrusel_asociado:
            raise ValidationError('Debes seleccionar un carrusel asociado si especificas una posición')

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
class EnlaceSeccionSobreNosotros(models.Model):
    TIPO_ENLACE_CHOICES = [
        ('YOUTUBE', 'YouTube'),
        ('INSTAGRAM', 'Instagram'),
        ('FACEBOOK', 'Facebook'),
        ('TWITTER', 'Twitter/X'),
        ('IMDB', 'IMDb'),
        ('OTRO', 'Otro'),
    ]
    
    seccion = models.ForeignKey(
        SeccionSobreNosotros, 
        related_name='enlaces', 
        on_delete=models.CASCADE
    )
    url = models.URLField()
    tipo = models.CharField(max_length=10, choices=TIPO_ENLACE_CHOICES)
    titulo = models.CharField(max_length=100, blank=True)
    icono = models.ImageField(
        upload_to='sobre_nosotros/iconos/', 
        blank=True, 
        null=True,
        help_text="Icono personalizado (opcional). Si no se sube, se usará el icono por defecto según el tipo."
    )
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Enlace de sección"
        verbose_name_plural = "Enlaces de sección"
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo or self.url}"
    
    def get_icon_class(self):
        iconos = {
            'YOUTUBE': 'fab fa-youtube',
            'INSTAGRAM': 'fab fa-instagram',
            'FACEBOOK': 'fab fa-facebook-f',
            'TWITTER': 'fab fa-twitter',
            'IMDB': 'fab fa-imdb',
            'OTRO': 'fas fa-external-link-alt',
        }
        return iconos.get(self.tipo, 'fas fa-link')
class ImagenCarrusel(models.Model):
    seccion = models.ForeignKey(
        SeccionSobreNosotros, 
        related_name='imagenes_del_carrusel',  # Nombre único
        on_delete=models.CASCADE
    )
    imagen = models.ImageField(upload_to='sobre_nosotros/carrusel/')
    titulo = models.CharField(max_length=100, blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Imágenes para Carruseles"

class ImagenCarruselSobreNosotros(models.Model):
    seccion = models.ForeignKey(
        SeccionSobreNosotros, 
        related_name='imagenes_carrusel',
        on_delete=models.CASCADE
    )
    imagen = models.ImageField(upload_to='sobre_nosotros/carrusel/')
    titulo = models.CharField(max_length=100, blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen de Carrusel"
        verbose_name_plural = "Imágenes de Carrusel"

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


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']
        
    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.fecha})"

