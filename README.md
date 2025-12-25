Стек:
Python 3.11
Django + DRF
PostgreSQL
Docker (для БД)
Как запустить проект локально
1. Клонировать репозиторий
git clone <REPO_URL>
cd secinc
2. Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate
3. Установить зависимости
pip install -r requirements.txt
4. Создать .env из примера
cp .env.example .env
При необходимости отредактировать значения в .env.
5. Запустить PostgreSQL через Docker
docker compose up -d
6. Применить миграции
python manage.py migrate
7. Создать администратора
python manage.py createsuperuser
8. Запустить сервер разработки
python manage.py runserver
Доступные URL
Назначение	URL
Главная	http://127.0.0.1:8000/
Инциденты	http://127.0.0.1:8000/incidents/
События	http://127.0.0.1:8000/events/
Отчёты	http://127.0.0.1:8000/reports/
Экспорт Excel	http://127.0.0.1:8000/reports/incidents.xlsx
Admin	http://127.0.0.1:8000/admin/
Swagger	http://127.0.0.1:8000/api/docs/
Переменные окружения
Файл .env.example содержит базовый набор переменных:
DEBUG=1
SECRET_KEY=change-me

DB_NAME=secinc
DB_USER=secinc_user
DB_PASSWORD=secinc_pass
DB_HOST=127.0.0.1
DB_PORT=5433
.env не коммитится и создаётся локально.

Требования
Python 3.11+
Docker + Docker Compose
Git
