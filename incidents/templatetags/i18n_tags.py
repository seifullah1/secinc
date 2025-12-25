from django import template
from incidents.i18n import t as translate

register = template.Library()

@register.filter
def tr(key, request):
    lang = getattr(request, "ui_lang", "ru")
    return translate(lang, key)
