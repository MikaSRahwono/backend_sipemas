from .base import *
import os
import datetime

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    '127.0.0.1',
]
CORS_ALLOW_ALL_ORIGINS = True

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
