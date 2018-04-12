from django.db import models
from django.conf import settings
from django.utils.http import urlencode
from django.utils import timezone


class Event(models.Model):
    # max length comes from their docs
    event_key = models.PositiveIntegerField()
    title = models.CharField(max_length=355)
    description = models.TextField()
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def link(self):
        return 'https://onlinexperiences.com/Launch/Event.htm?' + urlencode({
            'ShowKey': settings.INXPO_PARAMETERS['SHOW_KEY'],
            'DisplayItem': 'E' + str(self.event_key),
        })

    @property
    def image_url(self):
        if self.image.startswith('https://'):
            return self.image
        else:
            return 'https://onlinexperiences.com' + self.image

    @property
    def is_streaming_now(self):
        return self.starts_at <= timezone.now() <= self.ends_at
