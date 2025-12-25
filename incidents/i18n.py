TEXT = {
  "ru": {
    "dashboard": "Панель",
    "incidents": "Инциденты",
    "events": "События",
    "reports": "Отчёты",
    "logout": "Выход",
    "login": "Войти",
    "username": "Логин",
    "password": "Пароль",
    "soc_title": "SOC / ISMS Dashboard",
    "soc_sub": "Журнал инцидентов и событий безопасности предприятия",
    "download_excel": "Скачать Excel (.xlsx)",
    "incidents_excel": "Инциденты (Excel)",
  },
  "kk": {
    "dashboard": "Басқару панелі",
    "incidents": "Инциденттер",
    "events": "Оқиғалар",
    "reports": "Есептер",
    "logout": "Шығу",
    "login": "Кіру",
    "username": "Логин",
    "password": "Құпиясөз",
    "soc_title": "SOC / ISMS Басқару тақтасы",
    "soc_sub": "Кәсіпорынның қауіпсіздік оқиғалары мен инциденттері журналы",
    "download_excel": "Excel жүктеу (.xlsx)",
    "incidents_excel": "Инциденттер (Excel)",
  }
}

def t(lang: str, key: str) -> str:
    lang = "kk" if lang == "kk" else "ru"
    return TEXT.get(lang, TEXT["ru"]).get(key, key)
