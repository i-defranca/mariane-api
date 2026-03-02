from pathlib import Path

DIR = Path(__file__).resolve().parent.parent

DEBUG = True
SECRET_KEY = 'django-insecure-l_iute3z'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
        'NAME': 'DB_DATABASE',
        'USER': 'DB_USERNAME',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True
