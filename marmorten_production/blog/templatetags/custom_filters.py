from django import template
import os
from django.conf import settings

register = template.Library()

@register.filter
def file_exists(filepath):
    if not filepath:
        return False
    full_path = os.path.join(settings.MEDIA_ROOT, filepath.replace(settings.MEDIA_URL, ''))
    return os.path.exists(full_path)