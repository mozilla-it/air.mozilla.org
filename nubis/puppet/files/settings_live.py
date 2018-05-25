import os

from .settings import *

import imp
nubis = imp.load_source('nubis', '/etc/nubis-config/airmofront.sh')

DEBUG = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': nubis.Cache_Endpoint + ':' + nubis.Cache_Port,
        'KEY_PREFIX': 'airmozilla-live',
    }
}

ALLOWED_HOSTS = ['air.mozilla.org', nubis.SITE_HOSTNAME]

# Mozilla is deploying this, and db backups aren't necesary since it's
# generated on a schedule.
# BACKUPDB_DIRECTORY = os.environ['BACKUP_DIR']
STATIC_ROOT = os.environ['STATIC_ROOT']
SECRET_KEY = os.environ['SECRET_KEY']
COMPRESS_ENABLED = True
