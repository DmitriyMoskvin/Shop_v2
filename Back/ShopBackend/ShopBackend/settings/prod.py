from .base import *

DEBUG = False  # Отключаем дебаг

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASES_NAME'),        # Название таблицы PostgreSQL
        'USER': os.environ.get('DATABASES_USER'),        # Имя пользователя
        'PASSWORD': os.environ.get('DATABASES_PASSWORD'),
        'HOST': 'db',        # Или IP-адрес сервера PostgreSQL  ('db' потомучто в docker-compose теперь db)
        'PORT': 5432,        # Стандартный порт PostgreSQL
    }
}