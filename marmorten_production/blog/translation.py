from modeltranslation.translator import translator, TranslationOptions
from .models import Post, CarruselPost, GaleriaImagenes, Equipo, SeccionSobreNosotros


class PostTranslation(TranslationOptions):
    fields = ('title', 'content', 'resumen')

translator.register(Post, PostTranslation)


class CarruselPostTranslation(TranslationOptions):
    fields = ('titulo', 'descripcion')

translator.register(CarruselPost, CarruselPostTranslation)


class GaleriaImagenesTranslation(TranslationOptions):
    fields = ('titulo',)

translator.register(GaleriaImagenes, GaleriaImagenesTranslation)


class EquipoTranslation(TranslationOptions):
    fields = ('puesto', 'biografia')

translator.register(Equipo, EquipoTranslation)


class SeccionSobreNosotrosTranslation(TranslationOptions):
    fields = ('titulo', 'contenido_texto')

translator.register(SeccionSobreNosotros, SeccionSobreNosotrosTranslation)