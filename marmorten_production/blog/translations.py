from modeltranslation.translator import translator, TranslationOptions
from .models import Post, EnlaceExterno, Equipo

# Registrar las traducciones del modelo Post
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'resumen')

# Registrar las traducciones del modelo EnlaceExterno
class EnlaceExternoTranslationOptions(TranslationOptions):
    fields = ('titulo',)

# Registrar las traducciones del modelo Equipo
class EquipoTranslationOptions(TranslationOptions):
    fields = ('nombre', 'puesto', 'biografia')

# Registrando las clases de traducción
translator.register(Post, PostTranslationOptions)
translator.register(EnlaceExterno, EnlaceExternoTranslationOptions)
translator.register(Equipo, EquipoTranslationOptions)
