import collections

import requests
from lxml import objectify
import dateutil.parser
import pytz

from django.conf import settings


def setup_constants():
    global EVENT_API_BASE, SHOW_SETUP_API_BASE
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

setup_constants()


class INXPOAPIException(Exception):
    pass


class EventNotFoundException(INXPOAPIException):
    pass


def parse_api_datetime(s):
    d = dateutil.parser.parse(str(s))
    return pytz.timezone('US/Central').localize(d)


def retrieve_xml(url, session=requests.session()):
    response = session.get(url, timeout=30)
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
