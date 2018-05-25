import os

from .settings import *

import socket

import imp
nubis = imp.load_source('nubis', '/etc/nubis-config/airmofront.sh')

hostname = socket.gethostname()
public_ip = socket.gethostbyname(hostname)

DEBUG = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': nubis.Cache_Endpoint + ':' + nubis.Cache_Port,
        'KEY_PREFIX': 'airmozilla-live',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': nubis.Database_Name,
        'USER': nubis.Database_User,
        'PASSWORD': nubis.Database_Password,
        'HOST': nubis.Database_Server,
    }
}

INXPO_PARAMETERS = {
    'AUTH_CODE': nubis.inxpo_auth_code,
    'USER_CREDENTIALS': nubis.inxpo_user_credentials,
    # retrieved from https://api.onlinexperiences.com/scripts/Server.nxp?LASCmd=AI:4;F:APIUTILS!50500&APIUserAuthCode=***REMOVED***&APIUserCredentials=***REMOVED***&OpCodeList=F&OutputFormat=X
    'SHOW_KEY': 44908,
    'SHOW_PACKAGE_KEY': 99827,
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = nubis.APP_SECRET_KEY

ALLOWED_HOSTS = ['localhost', 'air.mozilla.org', 'air.allizom.org', nubis.SITE_HOSTNAME, public_ip]

# Mozilla is deploying this, and db backups aren't necesary since it's
# generated on a schedule.
# BACKUPDB_DIRECTORY = os.environ['BACKUP_DIR']
STATIC_ROOT = os.environ['STATIC_ROOT']
SECRET_KEY = os.environ['SECRET_KEY']
COMPRESS_ENABLED = True
