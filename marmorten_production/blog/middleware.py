from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class SetLanguageFromURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verificar si la URL comienza con un código de idioma conocido
        path = request.path_info.lstrip('/')
        lang_code = None
        
        # Comprobar si el primer segmento es un idioma soportado
        for code, _ in settings.LANGUAGES:
            if path.startswith(f'{code}/') or path == code:
                lang_code = code
                break
        
        # Si encontramos un idioma en la URL, establecerlo
        if lang_code and translation.check_for_language(lang_code):
            translation.activate(lang_code)
            request.LANGUAGE_CODE = translation.get_language()
            
            # Establecer la cookie de idioma personalizada
            response = self.get_response(request)
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,  # Usará 'Marmorten_language'
                lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE
            )
            
            # Para la sesión, usamos el nombre estándar que Django espera
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            
            return response
        
        return self.get_response(request)