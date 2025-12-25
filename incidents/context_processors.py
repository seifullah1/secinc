from .i18n import t

def ui_text(request):
    lang = getattr(request, "ui_lang", "ru")
    return {"t": lambda key: t(lang, key)}
