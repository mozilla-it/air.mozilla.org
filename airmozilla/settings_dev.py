import os

from .settings import *

DEBUG = False

# Hijack all emails and send them to the BANDIT_EMAIL address
EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'
BANDIT_EMAIL = 'bandit@fusionbox.com'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'airmozilla-dev',
    }
}

ALLOWED_HOSTS = ['airmozilla.dev.fusionbox.com']

BACKUPDB_DIRECTORY = os.environ['BACKUP_DIR']
STATIC_ROOT = os.environ['STATIC_ROOT']
SECRET_KEY = os.environ['SECRET_KEY']
COMPRESS_ENABLED = True
