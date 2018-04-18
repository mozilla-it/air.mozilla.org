import re

from django.db import models
from django.conf import settings
from django.utils.http import urlencode
from django.utils import timezone
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.db.models.expressions import RawSQL


def process_query(s):
    """
    Converts the user's search string into something suitable for passing to
    to_tsquery. Allows prefix matches on the last word.
    """
    query = re.sub(r'[!\'()|&:\x00<>]', ' ', s).strip()
    if query:
        query = re.sub(r'\s+', ' & ', query)
        # Support prefix search on the last word. A tsquery of 'toda:*' will
        # match against any words that start with 'toda', which is good for
        # search-as-you-type.
        query += ':*'
    return query


class EventQuerySet(models.QuerySet):
    def search(self, query):
        query = process_query(query)
        return self.annotate(
            is_match=RawSQL("to_tsquery('english_unaccent', %s) @@ fulltext", [query]),
            rank=RawSQL("ts_rank_cd(fulltext, to_tsquery('english_unaccent', %s))", [query]),
        ).filter(
            is_match=True,
        ).order_by('-rank')


class Event(models.Model):
    # max length comes from their docs
    event_key = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=355)
    description = models.TextField()
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(db_index=True)
    fulltext = SearchVectorField()  # trigger, update_event_fulltext

    objects = EventQuerySet.as_manager()

    class Meta:
        indexes = [
            GinIndex(['fulltext']),
        ]

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

    def to_json(self):
        return {
            'title': self.title,
            'link': self.link,
        }
