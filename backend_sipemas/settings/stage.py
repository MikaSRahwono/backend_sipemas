from .base import *
import os
import datetime

# SECURITY WARNING: don't run with debug turned on in production!
print(os.getenv('ALLOWED_HOSTS', '').split(','))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
DEBUG = False
CORS_ALLOW_ALL_ORIGINS = True

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'sipemas-db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
