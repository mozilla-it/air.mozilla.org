from django.views.generic import TemplateView
from django.utils import timezone

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
