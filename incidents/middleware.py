from django.utils.deprecation import MiddlewareMixin

class UiPrefsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.ui_theme = request.COOKIES.get("theme", "dark")
        request.ui_lang = request.COOKIES.get("lang", "ru")
