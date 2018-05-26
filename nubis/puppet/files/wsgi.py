"""
WSGI config for airmozilla project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airmozilla.settings_nubis")

# Set Outbound Proxies

os.environ["http_proxy"]="http://proxy.service.consul:3128/"
os.environ["HTTPS_PROXY"]="http://proxy.service.consul:3128/"
os.environ["https_proxy"]="http://proxy.service.consul:3128/"
os.environ["HTTP_PROXY"]="http://proxy.service.consul:3128/"

application = get_wsgi_application()
