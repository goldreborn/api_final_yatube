# Название Проекта
api final

# Описание
Этот проект представляет собой API Django Rest Framework для управления подписками пользователей.

# Установка
1. Клонировать репозиторий
2. Установите требования с помощью `pip install -r requirements.txt`
3. Запустите миграцию с помощью `python manage.py migrate`.
4. Запустите сервер с помощью `python manage.py runserver`.

# Примеры
- GET `/follow/`: возвращает все подписки аутентифицированного пользователя.
- POST `/follow/`: подписывает аутентифицированного пользователя на пользователя, переданного в теле запроса.