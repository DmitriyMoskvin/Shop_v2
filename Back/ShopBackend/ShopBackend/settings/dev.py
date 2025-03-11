from .base import *

DEBUG = True  # Включаем дебаг

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASES_NAME'),        # Название таблицы PostgreSQL
        'USER': os.environ.get('DATABASES_USER'),        # Имя пользователя
        'PASSWORD': os.environ.get('DATABASES_PASSWORD'),
        'HOST': os.environ.get('DATABASES_HOST'),        # Или IP-адрес сервера PostgreSQL
        'PORT': 5432,        # Стандартный порт PostgreSQL
    }
}