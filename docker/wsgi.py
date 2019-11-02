"""
WSGI config for airmozilla project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import newrelic.agent
newrelic.agent.initialize()

import os

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
