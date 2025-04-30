import os
from django.urls import path, include


BASE_DIR = path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'tu-servidor-smtp'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email'
EMAIL_HOST_PASSWORD = 'tu-contraseña'
DEFAULT_FROM_EMAIL = 'tu-email'
