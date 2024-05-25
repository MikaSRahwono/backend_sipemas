from .base import *
from datetime import timedelta

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    '127.0.0.1',
]
CORS_ALLOW_ALL_ORIGINS = True
BASE_DIR = Path(__file__).resolve().parent.parent.parent


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'postgres',
       'USER': 'postgres',
       'PASSWORD': 'admin',
       'HOST': 'localhost',
       'PORT': '5433',
   }
}