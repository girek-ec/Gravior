"""
Configuración de Django (6.1) para el sitio corporativo GRAVIOR.

Los valores sensibles o dependientes del entorno se leen desde el archivo
.env (ver .env.example).

https://docs.djangoproject.com/en/6.1/topics/settings/
https://docs.djangoproject.com/en/6.1/ref/settings/
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=''):
    return [item.strip() for item in os.getenv(name, default).split(',') if item.strip()]


# Seguridad
# https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Falta SECRET_KEY en el archivo .env (ver .env.example).')

DEBUG = env_bool('DEBUG', default=False)

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', 'localhost,127.0.0.1')

CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')


# Aplicaciones

INSTALLED_APPS = [
    'apps.core.admin_site.GraviorAdminConfig',  # admin con grupos ordenados (apps/core/admin_site.py)
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps del proyecto (una por dominio de contenido)
    'apps.core',
    'apps.inicio',
    'apps.empresa',
    'apps.genetica',
    'apps.calidad',
    'apps.productos',
    'apps.infraestructura',
    'apps.equipo',
    'apps.aliados',
    'apps.actualidad',
    'apps.contacto',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gravior.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'gravior.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Validación de contraseñas
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Idioma y zona horaria
# Sitio solo en español. USE_I18N se mantiene activo para que el admin y los
# mensajes de Django se muestren en español; no se usan i18n_patterns.

LANGUAGE_CODE = 'es'

LANGUAGES = [
    ('es', 'Español'),
]

TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_TZ = True


# Archivos estáticos (assets de Crafto en static/)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos subidos desde el admin (subcarpetas por módulo dentro de media/)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Correo (MAILERS, Django 6.1+; los ajustes EMAIL_* de Django están obsoletos)
# En desarrollo se usa el backend de consola. En producción definir en .env
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend y los datos SMTP.
# Las variables del .env conservan sus nombres; aquí se traducen a MAILERS.
# https://docs.djangoproject.com/en/6.1/howto/mailers-migration/

EMAIL_BACKEND_PATH = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_OPTIONS = {}
if EMAIL_BACKEND_PATH == 'django.core.mail.backends.smtp.EmailBackend':
    # Solo el backend SMTP recibe estas opciones (los demás advierten si reciben opciones desconocidas).
    EMAIL_OPTIONS = {
        'host': os.getenv('EMAIL_HOST', 'localhost'),
        'port': int(os.getenv('EMAIL_PORT', '587')),
        'username': os.getenv('EMAIL_HOST_USER', ''),
        'password': os.getenv('EMAIL_HOST_PASSWORD', ''),
        'use_tls': env_bool('EMAIL_USE_TLS', default=True),
        'use_ssl': env_bool('EMAIL_USE_SSL', default=False),
        'timeout': int(os.getenv('EMAIL_TIMEOUT', '10')),
    }

MAILERS = {
    'default': {
        'BACKEND': EMAIL_BACKEND_PATH,
        'OPTIONS': EMAIL_OPTIONS,
    },
}

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'root@localhost')
