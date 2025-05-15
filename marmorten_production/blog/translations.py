# blog/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Post, SeccionSobreNosotros, ConfiguracionSitio, Equipo

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'resumen')

@register(SeccionSobreNosotros)
class SeccionSobreNosotrosTranslationOptions(TranslationOptions):
    fields = ('titulo', 'contenido_texto')

@register(ConfiguracionSitio)
class ConfiguracionSitioTranslationOptions(TranslationOptions):
    fields = ('titulo_sitio', 'sobre_nosotros', 'mision', 'vision', 'direccion')

@register(Equipo)
class EquipoTranslationOptions(TranslationOptions):
    fields = ('nombre', 'puesto', 'biografia')