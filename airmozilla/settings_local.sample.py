from __future__ import absolute_import
"""
To use this, create a `.env` with DJANGO_SETTINGS_MODULE=airmozilla.settings_local
"""

from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
