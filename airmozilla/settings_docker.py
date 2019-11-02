import os

from .settings import *

DEBUG = True
ALLOWED_HOSTS = [ '*' ]

# XXX: Needs changing

#SECRET_KEY = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER':  os.getenv('DATABASE_USERNAME'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'CONN_MAX_AGE': 60,
    }
}

INXPO_PARAMETERS = {
    'AUTH_CODE': os.getenv('INXPO_AUTH_CODE'),
    'USER_CREDENTIALS': os.getenv('INXPO_USER_CREDENTIALS'),
    'SHOW_KEY': os.getenv('INXPO_SHOW_KEY'),
    'SHOW_PACKAGE_KEY': os.getenv('INXPO_SHOW_PACKAGE_KEY'),
}

COMPRESS_ENABLED = True
COMPRESS_OFFILNE = True

SECURE_HSTS_SECONDS = 86400
