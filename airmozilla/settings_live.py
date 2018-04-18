import os

from .settings import *

DEBUG = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'airmozilla-live',
    }
}

ALLOWED_HOSTS = ['air.mozilla.org']

# Mozilla is deploying this, and db backups aren't necesary since it's
# generated on a schedule.
# BACKUPDB_DIRECTORY = os.environ['BACKUP_DIR']
STATIC_ROOT = os.environ['STATIC_ROOT']
SECRET_KEY = os.environ['SECRET_KEY']
COMPRESS_ENABLED = True
