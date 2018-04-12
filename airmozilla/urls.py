"""airmozilla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
import django.views.generic

from . import views


class SettingsTemplateView(django.views.generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super(SettingsTemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context


urlpatterns = [
    url('^robots.txt$', SettingsTemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'
    )),
    url('^$', views.IndexView.as_view()),
    # this URL is hardcoded in airmozilla.js
    url('^load-more/$', views.LoadMoreEventsView.as_view()),
]
