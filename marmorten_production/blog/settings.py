import os
from django.urls import path, include


BASE_DIR = path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Configuración de Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.tuservidor.com'  # Ej: smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu@email.com'
EMAIL_HOST_PASSWORD = 'tupassword'
DEFAULT_FROM_EMAIL = 'no-reply@marmorten.com'

