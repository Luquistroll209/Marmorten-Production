from django.contrib import admin
from django.utils.html import format_html
from .models import Post, CarruselPost, GaleriaImagenes, Equipo, ConfiguracionSitio, SeccionPersonalizable, ImagenCarrusel

# ===== CLASE BASE PARA TODOS LOS ADMINS =====
class BaseAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }

# ===== ADMINISTRACIÓN DE POSTS =====
class GaleriaPostInline(admin.StackedInline):
    model = GaleriaImagenes
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height:100px; display:block; margin:0 auto;"/>',
                obj.imagen.url
            )
        return "-"
    preview.short_description = "Vista Previa"

@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('title', 'fecha_publicacion', 'destacado', 'mostrar_en_carrusel', 'imagen_preview')
    list_editable = ('destacado', 'mostrar_en_carrusel')  # Corregido: campos que existen en list_display
    list_filter = ('destacado', 'mostrar_en_carrusel')
    search_fields = ('title', 'content')
    inlines = [GaleriaPostInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'resumen', 'content')
        }),
        ('Configuraciones', {
            'fields': ('destacado', 'mostrar_en_carrusel', 'orden'),
            'classes': ('collapse',)
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video')
        })
    )
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height:50px; border-radius:4px;"/>',
                obj.imagen.url
            )
        return "-"
    imagen_preview.short_description = "Miniatura"

# ===== ADMINISTRACIÓN DE SECCIONES =====
class ImagenCarruselInline(admin.StackedInline):
    model = ImagenCarrusel
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height:100px; display:block; margin:0 auto;"/>',
                obj.imagen.url
            )
        return "-"
    preview.short_description = "Vista Previa"

@admin.register(SeccionPersonalizable)
class SeccionAdmin(BaseAdmin):
    list_display = ('titulo', 'get_tipo_display', 'orden', 'preview_content')  # Corregido: usando get_FOO_display
    list_editable = ('orden',)
    list_filter = ('tipo',)
    inlines = [ImagenCarruselInline]
    
    fieldsets = (
        ('Configuración', {
            'fields': ('titulo', 'tipo', 'orden')
        }),
        ('Contenido', {
            'fields': ('formato_texto', 'contenido_texto', 'imagen', 'enlace_url'),
            'classes': ('collapse',)
        })
    )
    
    def preview_content(self, obj):
        if obj.tipo == 'IMAGEN' and obj.imagen:
            return format_html(
                '<img src="{}" style="max-height:50px; border:1px solid #eee;"/>',
                obj.imagen.url
            )
        elif obj.tipo == 'TEXTO':
            return obj.contenido_texto[:50] + "..." if obj.contenido_texto else "-"
        elif obj.tipo == 'CAROUSEL':
            count = obj.imagenes_carrusel.count()
            return f"{count} imagen{'es' if count != 1 else ''}"
        elif obj.tipo == 'ENLACE':
            return obj.enlace_url[:30] + "..." if obj.enlace_url else "-"
        return "-"
    preview_content.short_description = "Vista Previa"

# ===== ADMINISTRACIÓN DEL EQUIPO =====
@admin.register(Equipo)
class EquipoAdmin(BaseAdmin):
    list_display = ('nombre', 'puesto', 'orden', 'foto_preview')
    list_editable = ('orden',)
    search_fields = ('nombre', 'puesto')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'puesto', 'biografia')
        }),
        ('Multimedia', {
            'fields': ('foto', 'redes_sociales')
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

# ===== CONFIGURACIÓN GLOBAL =====
@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(BaseAdmin):
    list_display = ('titulo_sitio', 'email_contacto', 'logo_preview')
    
    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:50px;"/>',
                obj.logo.url
            )
        return "-"
    logo_preview.short_description = "Logo"
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo_sitio', 'logo', 'email_contacto', 'telefono_contacto')
        }),
        ('Contenido', {
            'fields': ('sobre_nosotros', 'mision', 'vision')
        }),
        ('Redes Sociales', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url')
        })
    )

# ===== CARRUSEL PRINCIPAL =====
@admin.register(CarruselPost)
class CarruselPostAdmin(BaseAdmin):
    list_display = ('post', 'titulo', 'orden', 'activo')
    list_editable = ('orden', 'activo')
    list_filter = ('activo',)
    search_fields = ('post__title', 'titulo')