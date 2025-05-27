from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import (
    Post, CarruselPost, GaleriaImagenes, Equipo, ConfiguracionSitio,
    ImagenGaleriaSobreNosotros, ImagenCarruselSobreNosotros, SeccionSobreNosotros,
    ImagenCarrusel, MensajeContacto, EnlaceExterno, TelefonoContacto, EnlaceSeccionSobreNosotros, TipoTrabajo
)
import json
from modeltranslation.admin import TranslationAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

admin.site.site_header = 'Marmorten Productión'
admin.site.index_title = 'Panel de Administración'
from ckeditor.widgets import CKEditorWidget
from django import forms

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


class EnlaceSeccionInline(admin.StackedInline):
    model = EnlaceSeccionSobreNosotros
    extra = 1
    fields = ('tipo', 'url', 'titulo', 'icono', 'orden')

    def preview(self, obj):
        if obj.icono:
            return format_html(
                '<img src="{}" style="max-height:50px;"/>',
                obj.icono.url
            )
        return "-"
    preview.short_description = "Vista previa"


# ===== CONFIGURACIÓN DEL SITIO =====
class TelefonoContactoInline(admin.StackedInline):
    model = TelefonoContacto
    extra = 1
    fields = ('numero', 'descripcion', 'orden')
@admin.register(TipoTrabajo)
class TipoTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'orden')
    list_display_en = ('nombre', 'slug', 'orden')
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ('orden',)

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    
    inlines = [TelefonoContactoInline]
    list_display = ('titulo_sitio', 'email_contacto', 'preview_logo')

    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def preview_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.logo.url)
        return "-"

    preview_logo.short_description = "Logo"

    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo_sitio', 'logo', 'email_contacto', 'direccion', 'descripcion', 'descripcion_en')
        }),
        ('Redes Sociales', {
            'fields': ('imb_url', 'instagram_url', 'youtube_url')
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
            raise forms.ValidationError("Formato JSON inválido")


class EnlaceExternoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1
    fields = ('url', 'tipo', 'titulo', 'mostrar', 'orden')


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    inlines = [GaleriaPostInline, EnlaceExternoInline]
    list_display = ('title', 'fecha_publicacion', 'destacado', 'tipo_trabajo', 'destacado', 'tipo_trabajo')  # Añade tipo_trabajo aquí
    list_filter = ('destacado', 'tipo_trabajo')  # Añade filtro por tipo de trabajo

    fieldsets = (
        ('Contenido (Español)', {
            'fields': ('title','tipo_trabajo', 'resumen', 'content')
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video')
        }),
        ('Configuración', {
            'fields': ('destacado', 'mostrar_en_carrusel', 'orden'),  # Añade tipo_trabajo aquí
            'classes': ('collapse',)
        })
    )

    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height:50px; border-radius:4px;"/>', obj.imagen.url)
        return "-"

    preview.short_description = "Miniatura"


# ===== ADMINISTRACIÓN DEL EQUIPO =====
class EnlaceExternoEquipoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1
    fields = ('url', 'tipo', 'titulo', 'mostrar', 'orden')
    fk_name = 'equipo'


@admin.register(Equipo)
class EquipoAdmin(BaseAdmin, TranslationAdmin):
    list_display = ('nombre', 'puesto', 'orden', 'foto_preview')
    list_editable = ('orden',)
    search_fields = ('nombre', 'puesto')
    inlines = [EnlaceExternoEquipoInline]

    fieldsets = (
        ('Información (Español)', {
            'fields': ('nombre', 'puesto', 'biografia', 'foto')
        }),
        ('Configuración', {
            'fields': ('orden',)
        })
    )

    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height:50px; border-radius:50%;"/>', obj.foto.url)
        return "-"

    foto_preview.short_description = "Foto"


# ===== CARRUSEL PRINCIPAL =====
class PostAdminForm(forms.ModelForm):
    enlaces_externos = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False,
        help_text="""Formato JSON: [{
            "url": "https://ejemplo.com ",
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
class CarruselPostAdmin(TranslationAdmin):
    list_display = ('titulo', 'post', 'orden', 'activo')
    list_editable = ('orden', 'activo')

    fieldsets = (
        ('Información Básica (Español)', {
            'fields': ('post', 'titulo', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('orden', 'activo')
        })
    )

    def preview(self, obj):
        if obj.post and obj.post.imagen:
            return format_html('<img src="{}" style="max-height:50px; border-radius:4px;"/>', obj.post.imagen.url)
        return "-"

    preview.short_description = "Miniatura del Post"


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
class SeccionSobreNosotrosAdmin(TranslationAdmin):
    list_display = ('titulo', 'tipo', 'carrusel_asociado', 'posicion_carrusel', 'orden', 'preview_content')
    list_editable = ('orden', 'posicion_carrusel')
    list_filter = ('tipo', 'posicion_carrusel')
    inlines = [ImagenCarruselInline]

    
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'tipo','carrusel_asociado', 'posicion_carrusel', 'contenido_texto', 'imagen')
        }),
        ('Orden', {
            'fields': ('orden',)
        }),
    )

    def get_inlines(self, request, obj):
        if obj and obj.tipo == 'REDES':
            return [EnlaceSeccionInline]
        return super().get_inlines(request, obj)

    def preview_content(self, obj):
        if obj.tipo == 'TEXTO':
            texto = obj.contenido_texto_en if obj.contenido_texto_en else obj.contenido_texto
            return texto[:100] + "..." if texto else "-"
        elif obj.tipo == 'IMAGEN' and obj.imagen:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.imagen.url)
        elif obj.tipo == 'CAROUSEL':
            return f"{obj.imagenes_del_carrusel.count()} imágenes"
        elif obj.tipo == 'PORTADA':
            return "Portada principal"
        elif obj.tipo == 'REDES':
            return f"{obj.enlaces.count()} enlaces"
        return "-"

    preview_content.short_description = "Contenido"


# ===== OTROS MODELOS =====
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha', 'leido')
    list_filter = ('leido', 'fecha')
    search_fields = ('nombre', 'email', 'asunto')
    readonly_fields = ('fecha',)