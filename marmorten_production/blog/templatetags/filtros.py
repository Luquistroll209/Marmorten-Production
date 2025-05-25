
import re
import html
from django import template
from django.utils.text import Truncator

register = template.Library()

@register.filter
def limpiar_y_resumir(texto, num_palabras=30):
    texto_sin_html = re.sub(r'<[^>]*?>', '', texto or '')
    texto_decodificado = html.unescape(texto_sin_html)
    return Truncator(texto_decodificado).words(num_palabras)
