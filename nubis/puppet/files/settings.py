import os

from .settings import *

import socket
import os

import imp
nubis = imp.load_source('nubis', '/etc/nubis-config/airmofront.sh')

hostname = socket.gethostname()
public_ip = socket.gethostbyname(hostname)

DEBUG = False

if hasattr(nubis, 'DEBUG'):
  DEBUG = nubis.DEBUG.lower() in ("true", "1")

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
    # retrieved from https://api.onlinexperiences.com/scripts/Server.nxp?LASCmd=AI:4;F:APIUTILS!50500&APIUserAuthCode=chiathlunletrieswle5oaproableS&APIUserCredentials=vi7ciuslap8las71adoepleth5uyIa&OpCodeList=F&OutputFormat=X
    'SHOW_KEY': 44908,
    'SHOW_PACKAGE_KEY': 99827,
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = nubis.APP_SECRET_KEY

ALLOWED_HOSTS = ['localhost', 'air.mozilla.org', 'air.allizom.org', nubis.SITE_HOSTNAME, public_ip]

COMPRESS_ENABLED = True
COMPRESS_OFFILNE = True

SECURE_HSTS_SECONDS = 86400
