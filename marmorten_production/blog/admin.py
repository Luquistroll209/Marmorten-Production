from django.contrib import admin
from django.utils.html import format_html
from .models import Post, CarruselPost, GaleriaImagenes, Equipo, ConfiguracionSitio

class GaleriaImagenesInline(admin.TabularInline):
    model = GaleriaImagenes
    extra = 1
    fields = ['imagen', 'titulo', 'orden', 'preview']
    readonly_fields = ['preview']
    
    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imagen.url)
        return "-"
    preview.short_description = "Vista previa"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'tiene_imagen', 'fecha_publicacion', 'destacado', 'mostrar_en_carrusel', 'preview']
    list_editable = ['destacado', 'mostrar_en_carrusel']
    search_fields = ['title', 'content']
    inlines = [GaleriaImagenesInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'resumen', 'content', 'fecha_publicacion')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video')
        }),
        ('Configuraciones', {
            'fields': ('destacado', 'mostrar_en_carrusel', 'orden'),
            'classes': ('collapse',)
        }),
    )
    
    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.imagen.url)
        return "-"
    preview.short_description = "Imagen"

@admin.register(CarruselPost)
class CarruselPostAdmin(admin.ModelAdmin):
    list_display = ['post', 'titulo', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    list_filter = ['activo']
    search_fields = ['post__title', 'titulo']

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puesto', 'orden', 'foto_preview']
    list_editable = ['orden']
    search_fields = ['nombre', 'puesto']
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.foto.url)
        return "-"
    foto_preview.short_description = "Foto"

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.logo.url)
        return "-"
    logo_preview.short_description = "Logo"