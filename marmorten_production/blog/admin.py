from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import (
    Post, 
    CarruselPost, 
    GaleriaImagenes, 
    Equipo, 
    ConfiguracionSitio,
    ImagenGaleriaSobreNosotros,
    ImagenCarruselSobreNosotros,
    SeccionSobreNosotros,
    ImagenCarrusel,
    MensajeContacto,
    EnlaceExterno,

)
import json

admin.site.site_header = 'Marmorten Productión'
admin.site.index_title = 'Panel de Administración'

class BaseAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

class PreviewImageMixin:
    def preview(self, obj):
        if getattr(obj, 'imagen', None):
            return format_html(
                '<img src="{}" style="max-height:100px; display:block; margin:0 auto;"/>',
                obj.imagen.url
            )
        return "-"
    preview.short_description = "Vista Previa"

# ===== GALERÍA SOBRE NOSOTROS =====
class GaleriaSobreNosotrosInline(admin.StackedInline, PreviewImageMixin):
    model = ImagenGaleriaSobreNosotros
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)

# ===== CONFIGURACIÓN DEL SITIO =====
@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(BaseAdmin):
    list_display = ('titulo_sitio', 'email_contacto', 'preview_logo')
    inlines = [GaleriaSobreNosotrosInline]
    
    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def preview_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:50px;"/>',
                obj.logo.url
            )
        return "-"
    preview_logo.short_description = "Logo"
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo_sitio', 'logo', 'email_contacto', 'telefono_contacto', 'direccion')
        }),
        ('Redes Sociales', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url')
        })
    )

# ===== ADMINISTRACIÓN DE POSTS =====
class GaleriaPostInline(admin.StackedInline, PreviewImageMixin):
    model = GaleriaImagenes
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        
    def clean_enlaces_externos(self):
        data = self.cleaned_data.get('enlaces_externos', '[]')
        try:
            if isinstance(data, str):
                return json.loads(data)
            return data
        except json.JSONDecodeError:
            raise forms.ValidationError("Formato JSON inválido. Ejemplo: [{'url':'...','tipo':'YOUTUBE','mostrar_video':true}]")

class EnlaceExternoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1
    fields = ('url', 'tipo', 'titulo', 'mostrar', 'orden')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [GaleriaPostInline, EnlaceExternoInline]
    
    list_display = ('title', 'fecha_publicacion', 'destacado')
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'resumen', 'content')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video') 
        }),
        ('Configuración', {
            'fields': ('destacado', 'mostrar_en_carrusel', 'orden'),
            'classes': ('collapse',)
        })
    )
    
    def preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height:50px; border-radius:4px;"/>',
                obj.imagen.url
            )
        return "-"
    preview.short_description = "Miniatura"

# ===== ADMINISTRACIÓN DEL EQUIPO =====
@admin.register(Equipo)
class EquipoAdmin(BaseAdmin):
    list_display = ('nombre', 'puesto', 'orden', 'foto_preview')
    list_editable = ('orden',)
    search_fields = ('nombre', 'puesto')
    
    fieldsets = (
        ('Información', {
            'fields': ('nombre', 'puesto', 'biografia', 'redes_sociales')
        }),
        ('Imagen', {
            'fields': ('foto',)
        }),
        ('Configuración', {
            'fields': ('orden',),
            'classes': ('collapse',)
        })
    )
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" style="max-height:50px; border-radius:50%;"/>',
                obj.foto.url
            )
        return "-"
    foto_preview.short_description = "Foto"

# ===== CARRUSEL PRINCIPAL =====
class PostAdminForm(forms.ModelForm):
    enlaces_externos = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        help_text="""Formato JSON: [{
            "url": "https://ejemplo.com", 
            "tipo": "YOUTUBE/INSTAGRAM/FACEBOOK/TWITTER/OTRO", 
            "mostrar_video": true/false
        }]"""
    )
    
    def clean_enlaces_externos(self):
        data = self.cleaned_data['enlaces_externos']
        try:
            if data:
                return json.loads(data)
            return []
        except json.JSONDecodeError:
            raise forms.ValidationError("Formato JSON inválido")
@admin.register(CarruselPost)
class PostAdmin(BaseAdmin):
    form = PostAdminForm
    
    # Mantén tus list_display y otros atributos existentes
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'resumen', 'content')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video', 'enlaces_externos')
        }),
        ('Configuración', {
            'fields': ('destacado', 'mostrar_en_carrusel', 'orden'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if 'enlaces_externos' in form.cleaned_data:
            obj.enlaces_externos = form.cleaned_data['enlaces_externos']
        super().save_model(request, obj, form, change)

class ImagenCarruselSobreNosotrosInline(admin.StackedInline, PreviewImageMixin):
    model = ImagenCarruselSobreNosotros
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)

class ImagenCarruselInline(admin.StackedInline):
    model = ImagenCarrusel
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height:100px;"/>', obj.imagen.url)
        return "-"
    preview.short_description = "Vista previa"


@admin.register(SeccionSobreNosotros)
class SeccionSobreNosotrosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'orden', 'preview_content')
    list_editable = ('orden',)
    list_filter = ('tipo',)
    inlines = [ImagenCarruselInline]  # Solo para secciones de tipo carrusel
    
    def preview_content(self, obj):
        if obj.tipo == 'TEXTO':
            return obj.contenido_texto[:100] + "..." if obj.contenido_texto else "-"
        elif obj.tipo == 'IMAGEN' and obj.imagen:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.imagen.url)
        elif obj.tipo == 'CAROUSEL':
            return f"{obj.imagenes_del_carrusel.count()} imágenes"
        elif obj.tipo == 'PORTADA':
            return "Portada principal"
        return "-"
    preview_content.short_description = "Contenido"


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha', 'leido')
    list_filter = ('leido', 'fecha')
    search_fields = ('nombre', 'email', 'asunto')
    readonly_fields = ('fecha',)
