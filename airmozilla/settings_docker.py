import os

from .settings import *

DEBUG = True
ALLOWED_HOSTS = [ "*" ]

# XXX: Needs changing

#SECRET_KEY = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER':  os.getenv('DATABASE_USERNAME'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
    }
}

COMPRESS_ENABLED = True
COMPRESS_OFFILNE = True

SECURE_HSTS_SECONDS = 86400
