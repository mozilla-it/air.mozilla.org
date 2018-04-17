from django.views.generic import TemplateView, View
from django.utils import timezone
from django.http import Http404, JsonResponse

from .models import Event


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # List this because the template slices it and we don't want to do more
        # queries.
        context['upcoming_events'] = list(Event.objects.filter(
            ends_at__gte=timezone.now()
        ).order_by('starts_at'))
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

        # The page size (16) is hardcoded in airmozilla.js
        context['events'] = Event.objects.filter(
            ends_at__lt=timezone.now()
        ).order_by('-ends_at')[offset:offset + 16]

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
