from django import template
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag
def get_translated(obj, field):
    lang = get_language()
    field_name = f"{field}_{lang}"
    value = getattr(obj, field_name, None)
    
    # Si no hay valor en el idioma actual, usar español
    if not value and lang != 'es':
        field_name_es = f"{field}_es"
        value = getattr(obj, field_name_es, None)
    
    return value or ""