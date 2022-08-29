# Парсер cian

Стек технологий:
- Python 3.9.5
- PostgreSQL 14
- SQLAlchemy 1.4.40

Необходимо загрузить все библиотеки из файла requirements.txt

Для подключения к БД в файле database.py в create_engine нужно изменить на свои значения, где "postgres" - имя пользователя, "1z3q2w" - пароль пользователя, "cian" - название БД.

Для создания таблиц в БД необходимо запустить файл database.py

Доступны 2 региона - Новосибирск и Санкт-Петербург.

Для сбора списка ссылок на объявления использовались selenium и undetected-chromedriver

Для сбора данных из списка ссылок на объявления использовались requests и bs4.