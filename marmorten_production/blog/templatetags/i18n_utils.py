from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_redirect_url(context, lang_code):
    request = context['request']
    path = request.path

    supported_langs = [code for code, name in context.get('LANGUAGES', [])]
    lang_prefix = f'/{request.LANGUAGE_CODE}/'

    # Limpiar el prefijo actual si existe
    if len(path) > 3 and path[1:3] in supported_langs:
        path = '/' + '/'.join(path.split('/')[2:])  # Quitar /xx/

    # Si el nuevo idioma NO es el por defecto, agregarle el prefijo
    if lang_code != 'es':  # 'es' es tu idioma por defecto
        return f'/{lang_code}{path}'
    
    return path