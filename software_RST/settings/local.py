"""
Django settings for software_RST project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('KEEP_THE_SECRET_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
    'app.imprimir',

    # alertas
    'app.alertas',

    'app.cliente_proveedor.persona',
    'app.cliente_proveedor.cliente',
    'app.cliente_proveedor.proveedor',
    
    # clientes o proveedores-abc/creditos/historial
    # productos-abc
    'app.productos.detalle',
    'app.productos.marca',
    'app.productos.producto',
    'app.productos.inventario.historial',

    'app.productos.inventario.inventario',
    'app.productos.inventario.compras', 
    'app.productos.inventario.orden', 

    #banco
    'app.bancos.banco',
    'app.bancos.cuentas_por_cobrar',
    # 'app.bancos.chequera',
    

    # sistema/admin-bodega-ventas-cobros-conta
    'app.sistema.administrador.administrador',
    'app.sistema.usuarios',
    'app.sistema.tienda',

    'app.sistema.bodega.bodega',
    'app.sistema.bodega.traslados',

    'app.sistema.cobros.cobro',
    'app.sistema.cobros.caja',
    'app.sistema.cobros.contrasena',
    'app.sistema.cobros.depositos',

    'app.sistema.ventas.facturacion',
    'app.proformas',

    'app.sistema.conta.conta',

    'app.envios',




    # sitio/otros
    'django_celery_beat',
    'django_celery_results',
    
    # 'djcelery',
    'channels',

    # S3 AWS
    'storages',

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'drealtime.middleware.iShoutCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'software_RST.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'plantillas')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'software_RST.wsgi.application'




# ------------------------------------------------------------------
# -------------------------BASE DE DATOS----------------------------
# ------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':os.getenv("DB_RST_NAME"),
        'USER':os.getenv("DB_RST_USER"),
        'PASSWORD':os.getenv("DB_RST_PASSWORD"),
        'HOST':os.getenv("DB_RST_HOST"),
        'PORT':os.getenv("DB_RST_PORT"),
    }
}

# ------------------------------------------------------------------
# -------------------------BASE DE DATOS----------------------------
# ------------------------------------------------------------------



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "DB":1,
        },
        "KEY_PREFIX": "example"
    }
}

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-gt'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ------------------------------------------------------------------
# ---------------------------ESTATICOS------------------------------
# ------------------------------------------------------------------


STATIC_URL = '/estatico/'
STATIC_ROOT =os.path.join(os.path.dirname(BASE_DIR),"contenido_estatico")

STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"estatico"),
]




# ------------------------------------------------------------------
# -----------------------------MEDIA--------------------------------
# ------------------------------------------------------------------


MEDIA_URL ='/media/'
MEDIA_ROOT =os.path.join(os.path.dirname(BASE_DIR),"contenido_media")


from django.core.urlresolvers import reverse_lazy


LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL =reverse_lazy('login')
LOGOUT = reverse_lazy('logout')




CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 

CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0


BROKER_URL = 'redis://localhost:6379/0'  

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],  # set redis address
        },
        "ROUTING": "software_RST.settings.routing.channel_routing",  # load routing from our routing.py file
    },
}


# .

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('SMTP_EMAIL')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PORT = os.getenv('MAIL_PORT')

