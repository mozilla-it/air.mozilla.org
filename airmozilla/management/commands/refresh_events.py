import urllib.parse

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from airmozilla.models import Event
from airmozilla.inxpo import (
    retrieve_events, retrieve_privacy_strategy, parse_api_datetime,
    retrieve_event_time_range, EventNotFoundException
)


class Command(BaseCommand):
    help = 'Uses the INXPO API to refresh our database of events.'

    @transaction.atomic
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # This protectes against multiple refresh tasks running at the same
            # time, which could end up with duplicate copies of events. (DELETE
            # + INSERT is not a concurrency-safe way to replace the contents of
            # a table). This lock mode allows concurrent reads, so the frontend
            # is fine while we're refreshing.
            cursor.execute('LOCK TABLE %s IN EXCLUSIVE MODE' % Event._meta.db_table)

        Event.objects.all().delete()

        events = retrieve_events()
        privacy_strategy = retrieve_privacy_strategy()

        for event_node in events:
            if privacy_strategy.is_private(event_node):
                continue

            if event_node.Active == 0:
                continue

            try:
                time_range = retrieve_event_time_range(event_node.EventKey)
            except EventNotFoundException:
                # event was probably deleted since we retrieved the list
                continue

            assert time_range, "Event didn't have a start/end time when we expected it to."

            Event.objects.create(
                event_key=event_node.EventKey,
                title=urllib.parse.unquote(str(event_node.Description)),
                description=urllib.parse.unquote(str(event_node.Abstract)),
                created_at=parse_api_datetime(event_node.CreatedOnDate),
                image=event_node.IconImage,
                starts_at=time_range.starts_at,
                ends_at=time_range.ends_at,
            )
