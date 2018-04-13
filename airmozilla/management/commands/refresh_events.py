import collections
import urllib.parse

from django.core.management.base import BaseCommand
from django.db import transaction, connection
from django.conf import settings

import requests
from lxml import objectify
import dateutil.parser
import pytz

from airmozilla.models import Event


EVENT_API_BASE = (
    'https://api.onlinexperiences.com/scripts/Server.nxp?'
    # this parameter must come first
    'LASCmd=AI:4;F:APIUTILS!50540&'
    'APIUserAuthCode={AUTH_CODE}&'
    'APIUserCredentials={USER_CREDENTIALS}&'
    'ShowKey={SHOW_KEY}&'
    'OutputFormat=X'
).format(**settings.INXPO_PARAMETERS)


SHOW_SETUP_API_BASE = (
    'https://api.onlinexperiences.com/scripts/Server.nxp?'
    # this parameter must come first
    'LASCmd=AI:4;F:APIUTILS!50565&'
    'APIUserAuthCode={AUTH_CODE}&'
    'APIUserCredentials={USER_CREDENTIALS}&'
    'ShowKey={SHOW_KEY}&'
    'OutputFormat=X'
).format(**settings.INXPO_PARAMETERS)


class INXPOAPIException(Exception):
    pass


class EventNotFoundException(INXPOAPIException):
    pass


def parse_api_datetime(s):
    d = dateutil.parser.parse(str(s))
    return pytz.timezone('US/Central').localize(d)


def retrieve_xml(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = objectify.fromstring(response.content)

    if data.tag == 'CallFailed':
        raise INXPOAPIException(data.get('Diag'))

    if data.get('OpCodesInError') not in {'0', None}:
        if hasattr(data, 'OpCodeResult'):
            message = data.OpCodeResult.get('Message')
            if data.OpCodeResult.get('Status') == '51':
                raise EventNotFoundException(message)
            else:
                raise INXPOAPIException(message)
        else:
            raise INXPOAPIException(data.get('APICallDiagnostic'))

    return data


def retrieve_events():
    event_list_data = retrieve_xml(EVENT_API_BASE + '&OpCodeList=EEL')
    return event_list_data.OpCodeResult.ResultRow


EventTimeRange = collections.namedtuple('EventTimeRange', [
    'starts_at', 'ends_at'
])


def retrieve_event_time_range(event_key):
    """
    Given an event key, returns its start and end times as a tuple of aware
    datetimes.
    """

    date_data = retrieve_xml(
        EVENT_API_BASE + '&OpCodeList=EDL&EventKey={}'.format(event_key)
    )

    for row in date_data.OpCodeResult.ResultRow:
        if row.DateType == 4:
            return EventTimeRange(
                starts_at=parse_api_datetime(row.FromDateTime),
                ends_at=parse_api_datetime(row.ToDateTime)
            )


class EventPrivacyStrategy(object):
    """
    Determines if an event is private based on the security group config.
    """

    def __init__(self, private_booth_keys, private_event_keys):
        self.private_booth_keys = private_booth_keys
        self.private_event_keys = private_event_keys

    def is_private(self, event):
        return (
            str(event.EventKey) in self.private_event_keys or
            str(event.BoothKey) in self.private_booth_keys
        )


def retrieve_privacy_strategy():
    security_group_data = retrieve_xml(SHOW_SETUP_API_BASE + '&InfoTypeFilter=|GE|GB|')

    # An event is non-public if it has any security group assignment, either
    # channel (BoothKey) or program (EventKey).

    private_booth_keys = set()
    private_event_keys = set()

    for channel_assignment in (
            security_group_data
            .SecurityGroupChannelAssignment
            .SecurityGroupChannelAssignment
    ):
        private_booth_keys.add(channel_assignment.get('BoothKey'))

    for program_assignment in (
            security_group_data
            .SecurityGroupProgramAssignment
            .SecurityGroupProgramAssignment
    ):
        private_event_keys.add(program_assignment.get('EventKey'))

    return EventPrivacyStrategy(
        private_booth_keys=private_booth_keys,
        private_event_keys=private_event_keys
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
