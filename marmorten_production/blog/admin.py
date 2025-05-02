from django.contrib import admin
from django.utils.html import format_html
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

)
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

@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('title', 'fecha_publicacion', 'destacado', 'mostrar_en_carrusel', 'preview')
    list_editable = ('destacado', 'mostrar_en_carrusel')
    list_filter = ('destacado', 'mostrar_en_carrusel')
    search_fields = ('title', 'content')
    inlines = [GaleriaPostInline]
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'resumen', 'content')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video', 'preview')
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
@admin.register(CarruselPost)
class CarruselPostAdmin(BaseAdmin):
    list_display = ('post', 'titulo', 'orden', 'activo')
    list_editable = ('orden', 'activo')
    list_filter = ('activo',)
    search_fields = ('post__title', 'titulo')

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
