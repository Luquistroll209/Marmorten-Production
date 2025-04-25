from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, CarruselEncabezado, ImagenCarrusel

class ImagenCarruselInline(admin.TabularInline):
    model = ImagenCarrusel
    extra = 1
    fields = ['imagen', 'titulo', 'enlace', 'orden', 'activo', 'preview']
    readonly_fields = ['preview']
    
    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.imagen.url)
        return "-"
    preview.short_description = "Vista previa"

class PostInline(admin.TabularInline):
    model = CarruselEncabezado.posts.through
    extra = 1
    verbose_name = "Post para carrusel"
    verbose_name_plural = "Posts para carrusel"

@admin.register(CarruselEncabezado)
class CarruselEncabezadoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'activo', 'efecto_transicion', 'velocidad_transicion']
    list_editable = ['activo']
    filter_horizontal = ['posts']
    inlines = [ImagenCarruselInline]
    fieldsets = (
        (None, {
            'fields': ('titulo', 'subtitulo', 'activo')
        }),
        ('Configuración del Carrusel', {
            'fields': ('velocidad_transicion', 'efecto_transicion')
        }),
    )

@admin.register(ImagenCarrusel)
class ImagenCarruselAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'preview', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    list_filter = ['activo']
    
    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.imagen.url)
        return "-"
    preview.short_description = "Vista previa"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'fecha_publicacion', 'destacado', 'mostrar_en_encabezado', 'preview']
    list_editable = ['destacado', 'mostrar_en_encabezado']
    search_fields = ['title', 'content']
    list_filter = ['destacado', 'mostrar_en_encabezado', 'fecha_publicacion']
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'fecha_publicacion')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video')
        }),
        ('Configuraciones Avanzadas', {
            'fields': ('destacado', 'orden_carrusel', 'mostrar_en_encabezado'),
            'classes': ('collapse',)
        }),
    )
    
    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.imagen.url)
        return "-"
    preview.short_description = "Imagen"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'aprobado']
    list_editable = ['aprobado']
    search_fields = ['author', 'content']
    list_filter = ['aprobado', 'created_at']
    actions = ['aprobar_comentarios']
    
    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"