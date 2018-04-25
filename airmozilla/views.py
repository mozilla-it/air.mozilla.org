from django.views.generic import TemplateView, View, RedirectView
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.conf import settings

from .models import Event
from .inxpo import get_anonymous_login_url_for_event, EventNotFoundException


class SettingsTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(SettingsTemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context


class IndexView(SettingsTemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # List this because the template slices it and we don't want to do more
        # queries.
        context['upcoming_events'] = list(Event.objects.filter(
            ends_at__gte=timezone.now()
        ).order_by('starts_at'))[:11]
        context['past_events'] = Event.objects.filter(
            ends_at__lt=timezone.now()
        ).order_by('-ends_at')[:6]
        return context


class LoadMoreEventsView(TemplateView):
    template_name = '_event_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            offset = self.request.GET['offset']
            offset = int(offset)
        except (KeyError, ValueError):
            raise Http404

        context['events'] = Event.objects.filter(
            ends_at__lt=timezone.now()
        ).order_by('-ends_at')[offset:offset + settings.PAGE_SIZE]

        return context


class SearchView(View):
    def get(self, request):
        try:
            search = request.GET['q']
        except KeyError:
            raise Http404

        events = Event.objects.search(search).defer(
            'fulltext', 'description'
        ).order_by('-rank')[:50]

        return JsonResponse({
            'results': [event.to_json() for event in events],
        })


class EventRedirectView(RedirectView):
    # The login ticket expires so this can't be permanent.
    permanent = False

    def get_redirect_url(self, event_key):
        try:
            return get_anonymous_login_url_for_event(event_key)
        except EventNotFoundException:
            raise Http404
