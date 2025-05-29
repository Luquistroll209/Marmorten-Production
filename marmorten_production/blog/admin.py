from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.urls import path, reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .models import (
    Post, CarruselPost, GaleriaImagenes, Equipo, ConfiguracionSitio,
    ImagenGaleriaSobreNosotros, ImagenCarruselSobreNosotros, SeccionSobreNosotros,
    ImagenCarrusel, MensajeContacto, EnlaceExterno, TelefonoContacto, 
    EnlaceSeccionSobreNosotros, TipoTrabajo
)
import json
from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget

# Configuración básica del sitio admin
admin.site.site_header = 'Marmoten Production - Panel de Administración'
admin.site.site_title = 'Marmoten Production'
admin.site.index_title = 'Bienvenido al Panel de Control'

# Estilos personalizados
class MarmotenAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Organiza las aplicaciones de manera más intuitiva
        """
        app_list = super().get_app_list(request)
        
        # Reorganizar las apps para un flujo más lógico
        ordered_apps = []
        custom_order = [
            'Configuración del Sitio',
            'Contenido Principal',
            'Sobre Nosotros',
            'Equipo',
            'Contacto'
        ]
        
        # Orden personalizado
        for app_name in custom_order:
            for app in app_list:
                if app['name'] == app_name:
                    ordered_apps.append(app)
                    break
        
        # Añadir las que no están en el orden personalizado
        for app in app_list:
            if app['name'] not in custom_order:
                ordered_apps.append(app)
                
        return ordered_apps
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('manual/', self.admin_view(self.manual_view), name='manual-usuario'),
        ]
        return custom_urls + urls
    
    @staff_member_required
    def manual_view(self, request):
        context = {
            **self.each_context(request),
            'title': 'Manual de Usuario - Marmoten Production',
        }
        return TemplateResponse(request, 'admin/manual_usuario.html', context)

# Registramos el sitio admin personalizado
admin_site = MarmotenAdminSite(name='marmoten_admin')

# Mixin para vistas previas de imágenes
class PreviewImageMixin:
    def preview(self, obj):
        if getattr(obj, 'imagen', None):
            return format_html(
                '<div style="text-align:center;"><img src="{}" style="max-height:100px; max-width:100%; border-radius:4px; box-shadow:0 2px 4px rgba(0,0,0,0.1);"/></div>',
                obj.imagen.url
            )
        return "-"
    preview.short_description = "Vista Previa"

# ===== CONFIGURACIÓN DEL SITIO =====
class TelefonoContactoInline(admin.StackedInline):
    model = TelefonoContacto
    extra = 1
    fields = ('numero', 'descripcion', 'orden')
    classes = ('collapse',)
    verbose_name = "Teléfono de Contacto"
    verbose_name_plural = "Teléfonos de Contacto"

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    inlines = [TelefonoContactoInline]
    list_display = ('titulo_sitio', 'email_contacto', 'preview_logo')
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo_sitio', 'logo', 'email_contacto', 'direccion', 
                      'descripcion', 'descripcion_en'),
            'classes': ('wide',)
        }),
        ('Redes Sociales', {
            'fields': ('imb_url', 'instagram_url', 'youtube_url'),
            'classes': ('wide', 'collapse')
        })
    )
    # Removed the custom change_form_template to use default template
    # change_form_template = 'admin/configuracion_change_form.html'

    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def preview_logo(self, obj):
        if obj.logo:
            return format_html(
                '<div style="text-align:center;"><img src="{}" style="max-height:50px; border-radius:4px;"/></div>',
                obj.logo.url
            )
        return "-"
    preview_logo.short_description = "Logo"

    def response_change(self, request, obj):
        if "_addanother" not in request.POST and "_continue" not in request.POST:
            return HttpResponseRedirect(reverse('admin:index'))
        return super().response_change(request, obj)

# ===== TIPOS DE TRABAJO =====
@admin.register(TipoTrabajo)
class TipoTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nombre_en', 'slug', 'orden', 'color_tag')
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ('orden',)
    list_editable = ('orden',)
    
    fieldsets = (
        ('Español', {
            'fields': ('nombre', 'nombre_en',)
        }),
        ('Configuración', {
            'fields': ('slug', 'orden')
        })
    )
    
    def color_tag(self, obj):
        colors = ['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7', '#C7CEEA']
        color = colors[obj.id % len(colors)] if obj.id else colors[0]
        return format_html(
            '<div style="background-color:{}; width:20px; height:20px; border-radius:50%; margin:0 auto;"></div>',
            color
        )
    color_tag.short_description = "Color"

# ===== POSTS Y CONTENIDO =====
class GaleriaPostInline(admin.StackedInline, PreviewImageMixin):
    model = GaleriaImagenes
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)
    verbose_name = "Imagen de Galería"
    verbose_name_plural = "Galería de Imágenes"

class EnlaceExternoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1
    fields = ('url', 'tipo', 'titulo', 'mostrar', 'orden')
    verbose_name = "Enlace Externo"
    verbose_name_plural = "Enlaces Externos"

@admin.register(Post)
class PostAdmin(TranslationAdmin):
    inlines = [GaleriaPostInline, EnlaceExternoInline]
    list_display = ('title', 'fecha_publicacion', 'destacado', 'tipo_trabajo', 'preview', 'status')
    list_filter = ('destacado', 'tipo_trabajo', 'fecha_publicacion')
    list_editable = ('destacado',)
    search_fields = ('title', 'content', 'resumen')
    date_hierarchy = 'fecha_publicacion'
    save_on_top = True
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'tipo_trabajo', 'resumen', 'content'),
            'classes': ('wide',)
        }),
        ('Multimedia', {
            'fields': ('imagen', 'video'),
            'classes': ('wide', 'collapse')
        }),
        ('Configuración', {
            'fields': ('destacado', 'mostrar_en_carrusel', 'fecha_publicacion', 'orden'),
            'classes': ('wide', 'collapse')
        })
    )

    def preview(self, obj):
        if obj.imagen:
            return format_html(
                '<div style="text-align:center;"><img src="{}" style="max-height:50px; border-radius:4px;"/></div>',
                obj.imagen.url
            )
        return "-"
    preview.short_description = "Imagen"

    def status(self, obj):
        now = timezone.now()
        if obj.fecha_publicacion > now:
            return format_html('<span style="color:orange; font-weight:bold;">Programado</span>')
        return format_html('<span style="color:green; font-weight:bold;">Publicado</span>')
    status.short_description = "Estado"

# ===== CARRUSEL PRINCIPAL =====
@admin.register(CarruselPost)
class CarruselPostAdmin(TranslationAdmin):
    list_display = ('titulo', 'post', 'orden', 'activo', 'preview')
    list_editable = ('orden', 'activo')
    list_filter = ('activo',)
    search_fields = ('titulo', 'post__title')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('post', 'titulo', 'descripcion'),
            'classes': ('wide',)
        }),
        ('Configuración', {
            'fields': ('orden', 'activo'),
            'classes': ('wide',)
        })
    )

    def preview(self, obj):
        if obj.post and obj.post.imagen:
            return format_html(
                '<div style="text-align:center;"><img src="{}" style="max-height:50px; border-radius:4px;"/></div>',
                obj.post.imagen.url
            )
        return "-"
    preview.short_description = "Imagen"

# ===== EQUIPO =====
class EnlaceExternoEquipoInline(admin.StackedInline):
    model = EnlaceExterno
    extra = 1
    fields = ('url', 'tipo', 'titulo', 'mostrar', 'orden')
    fk_name = 'equipo'
    verbose_name = "Red Social"
    verbose_name_plural = "Redes Sociales"

@admin.register(Equipo)
class EquipoAdmin(TranslationAdmin):
    list_display = ('nombre', 'puesto', 'orden', 'foto_preview')
    list_editable = ('orden',)
    search_fields = ('nombre', 'puesto')
    inlines = [EnlaceExternoEquipoInline]
    save_on_top = True
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'puesto', 'biografia', 'foto'),
            'classes': ('wide',)
        }),
        ('Configuración', {
            'fields': ('orden',),
            'classes': ('wide', 'collapse')
        })
    )

    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<div style="text-align:center;"><img src="{}" style="max-height:50px; border-radius:50%;"/></div>',
                obj.foto.url
            )
        return "-"
    foto_preview.short_description = "Foto"

# ===== SOBRE NOSOTROS =====
class ImagenCarruselInline(admin.StackedInline, PreviewImageMixin):
    model = ImagenCarrusel
    extra = 1
    fields = ('imagen', 'titulo', 'orden', 'preview')
    readonly_fields = ('preview',)
    verbose_name = "Imagen del Carrusel"
    verbose_name_plural = "Carrusel de Imágenes"

class EnlaceSeccionInline(admin.StackedInline):
    model = EnlaceSeccionSobreNosotros
    extra = 1
    fields = ('tipo', 'url', 'titulo', 'icono', 'orden')
    verbose_name = "Enlace"
    verbose_name_plural = "Enlaces"

@admin.register(SeccionSobreNosotros)
class SeccionSobreNosotrosAdmin(TranslationAdmin):
    list_display = ('titulo', 'tipo', 'orden', 'preview_content')
    list_editable = ('orden',)
    list_filter = ('tipo',)
    inlines = [ImagenCarruselInline]
    save_on_top = True
    
    fieldsets = (
        ('Contenido', {
            'fields': ('titulo', 'tipo', 'contenido_texto', 'imagen'),
            'classes': ('wide',)
        }),
        ('Carrusel Asociado', {
            'fields': ('carrusel_asociado', 'posicion_carrusel'),
            'classes': ('wide', 'collapse')
        }),
        ('Configuración', {
            'fields': ('orden',),
            'classes': ('wide', 'collapse')
        })
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
            return format_html(
                '<div style="text-align:center;"><img src="{}" style="max-height:50px;"/></div>',
                obj.imagen.url
            )
        elif obj.tipo == 'CAROUSEL':
            return f"{obj.imagenes_del_carrusel.count()} imágenes"
        elif obj.tipo == 'PORTADA':
            return "Portada principal"
        elif obj.tipo == 'REDES':
            return f"{obj.enlaces.count()} enlaces"
        return "-"
    preview_content.short_description = "Vista Previa"

# ===== MENSAJES DE CONTACTO =====
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha', 'leido', 'acciones')
    list_filter = ('leido', 'fecha')
    search_fields = ('nombre', 'email', 'asunto')
    readonly_fields = ('fecha',)
    date_hierarchy = 'fecha'
    actions = ['marcar_como_leido']
    
    def acciones(self, obj):
        return format_html(
            '<a href="{}" class="button" style="padding:5px 10px; background:#417690; color:white; border-radius:3px;">Ver</a>',
            reverse('admin:blog_mensajecontacto_change', args=[obj.id])
        )
    acciones.short_description = "Acciones"

    def marcar_como_leido(self, request, queryset):
        updated = queryset.update(leido=True)
        self.message_user(request, f"{updated} mensajes marcados como leídos.")
    marcar_como_leido.short_description = "Marcar como leído"