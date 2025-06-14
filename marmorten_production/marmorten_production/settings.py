"""
Django settings for marmorten_production project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bh4c+q0w8r7gp%&f!l4+-l6ggf6led$sm3%jwz56i@ned@q!-6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
handler404 = 'blog.views.custom_404'


CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# Application definition

INSTALLED_APPS = [
    #'admin_interface',
    'tailwind',
    'ckeditor',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'axes', 
    'rosetta',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'colorfield',
    'blog',
]
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage',  # Para subir imágenes
            'div',
            'autolink',
            'embed',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
}
ADMIN_INTERFACE = {
    'THEME': 'default',  # Puedes crear tus propios temas
    'LOGO': 'img/logo.png',
    'FAVICON': 'img/favicon.ico',
}
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  # Debe ser el primero
    'django.contrib.auth.backends.ModelBackend',
]

# Configuración adicional
AXES_FAILURE_LIMIT = 5  # Intentos fallidos antes de bloquear
AXES_COOLOFF_TIME = 1  # 1 hora de bloqueo
AXES_LOCK_OUT_AT_FAILURE = True
AXES_ONLY_USER_FAILURES = True
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost' 
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'no-reply@tudominio.com'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'blog.middleware.SetLanguageFromURLMiddleware',  # Middleware personalizado para establecer el idioma desde la URL  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',

    
]
ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'

ROSETTA_ACCESS_CONTROL_FUNCTION = 'blog.utils.rosetta_access'

ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True  
ROSETTA_WSGI_AUTO_RELOAD = True
ROSETTA_UWSGI_AUTO_RELOAD = True

ROOT_URLCONF = 'marmorten_production.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'marmorten_production.wsgi.application'

STATIC_URL = '/static/'
#STATIC_URL = '/config/'
#STATIC_URL = '/equipo/'
#STATIC_URL = '/galeria/'
#STATIC_URL = '/imagenes/'
#STATIC_URL = '/sobre_nosotros/'
#STATIC_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]
TIME_ZONE = 'UTC'
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),  # Directorio donde se guardarán las traducciones
]
USE_I18N = True
MODELTRANSLATION_LANGUAGES = ('es', 'en')  # Orden importante
MODELTRANSLATION_DEFAULT_LANGUAGE = 'es'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'es'


LANGUAGE_COOKIE_NAME = 'Marmorten_language' 
LANGUAGE_COOKIE_AGE = 365 * 24 * 60 * 60  # 1 año
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = 'Lax'

# Opcional: Para que no se vea "[es]" en los campos originales

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# Tema de dominios

CSRF_TRUSTED_ORIGINS = [
    'https://generate-met-evaluations-jump.trycloudflare.com',
]



ALLOWED_HOSTS = ['generate-met-evaluations-jump.trycloudflare.com', 'localhost', '127.0.0.1', '0.0.0.0', '37.27.200.230']



CORS_ALLOWED_ORIGINS = ["https://proven-main-mastodon.ngrok-free.app/"]