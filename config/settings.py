import os
from pathlib import Path

from dotenv import load_dotenv as load

from config.logs import setup_structlog

DIR = Path(__file__).resolve().parent.parent

load(DIR / '.env')

LOGGING = setup_structlog(DIR, os.getenv('LOG_LEVEL'))

IS_PRODUCTION = os.getenv('DJANGO_ENV') == 'PRODUCTION'

DEBUG = os.getenv('DEBUG') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')

CSRF_COOKIE_SECURE = IS_PRODUCTION
SECURE_SSL_REDIRECT = IS_PRODUCTION
SESSION_COOKIE_SECURE = IS_PRODUCTION
CORS_ALLOW_ALL_ORIGINS = not IS_PRODUCTION

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'corsheaders',
    'rest_framework',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_structlog',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_structlog.middlewares.RequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

DJANGO_STRUCTLOG = {'REQUEST_ID_HEADER': 'HTTP_X_REQUEST_ID'}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
}

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
        'NAME': os.getenv('DB_DATABASE'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')

USE_I18N = True
USE_TZ = True
