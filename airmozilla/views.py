from django.views.generic import TemplateView
from django.utils import timezone
from django.http import Http404

from .models import Event


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = Event.objects.filter(
            ends_at__gte=timezone.now()
        ).order_by('starts_at')
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

        # The page size (8) is hardcoded in airmozilla.js
        context['events'] = Event.objects.filter(
            ends_at__lt=timezone.now()
        ).order_by('-ends_at')[offset:offset + 8]

        return context
