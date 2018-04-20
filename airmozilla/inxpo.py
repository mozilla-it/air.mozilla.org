"""
Routines for connecting to INXPO. Docs:

EVENT_API_BASE:
https://docs.google.com/document/d/1wgd3_oy0g1LjE9wduJdeXDnAyhLQze9vTpC8w-FNwNw/edit?usp=sharing

USER_API_BASE, retrieve ShowKey:
https://docs.google.com/document/d/1boLmZj9DRljI4t0ZFiAThCSVSUW5vAdmsMpnyc3jAHA/edit?usp=sharing

SHOW_SETUP_API_BASE, retrieve ShowPackageKey:
https://docs.google.com/document/d/1qfcuAEe3TJbJppv-tFCrRq3ePH5eY30A-rJANpdLvcE/edit?usp=sharing
"""

import collections
import uuid

import requests
from lxml import objectify
import dateutil.parser
import pytz

from django.conf import settings
from django.utils.http import urlencode


def setup_constants():
    """This allows using override_settings in tests."""

    global EVENT_API_BASE, SHOW_SETUP_API_BASE, USER_API_BASE, LOGIN_TICKET_URL
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

    USER_API_BASE = (
        'https://api.onlinexperiences.com/scripts/Server.nxp?'
        'LASCmd=AI:4;F:APIUTILS!50500&'
        'APIUserAuthCode={AUTH_CODE}&'
        'APIUserCredentials={USER_CREDENTIALS}&'
        'ShowKey={SHOW_KEY}&'
        'OutputFormat=X'
    ).format(**settings.INXPO_PARAMETERS)

    LOGIN_TICKET_URL = (
        'https://api.onlinexperiences.com/scripts/Server.nxp?'
        'LASCmd=AI:4;F:APIUTILS!50505&LoginTicketKey={login_ticket}'
    )

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

    return data


def retrieve_events():
    event_list_data = retrieve_xml(EVENT_API_BASE + '&OpCodeList=EEL')

    if event_list_data.get('OpCodesInError') != '0':
        raise INXPOAPIException(event_list_data.get('APICallDiagnostic'))

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

    if date_data.get('OpCodesInError') != '0':
        if date_data.get('APICallResult') == '0':
            message = date_data.OpCodeResult.get('Message')
            if date_data.OpCodeResult.get('Status') == '51':
                raise EventNotFoundException(message)
            else:
                raise INXPOAPIException(message)
        else:
            raise INXPOAPIException(date_data.get('APICallDiagnostic'))

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

    if security_group_data.tag == 'CallFailed':
        raise INXPOAPIException(security_group_data.get('Diag'))

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


def get_anonymous_login_url_for_event(event_key):
    email = '{}@anonymous.mozilla.invalid'.format(uuid.uuid4())
    data = retrieve_xml(USER_API_BASE + '&' + urlencode({
        'OpCodeList': 'CrT',
        'ShowPackageKey': settings.INXPO_PARAMETERS['SHOW_PACKAGE_KEY'],
        'EMailAddress': email,
        'FirstName': 'Anonymous',
        'LastName': 'User',
        'ShowLaunchInitialDisplayItem': 'E{}'.format(event_key),
    }))
    if data.get('APICallResult') != '0':
        raise INXPOAPIException(data.get('APICallDiagnostic'))

    if data.get('OpCodesProcessed') != '3':
        raise EventNotFoundException()

    for row in data.OpCodeResult:
        if row.get('Status') != '0':
            if row.get('OpCode') == 'T' and row.get('Status') == '76':
                raise EventNotFoundException(row.get('Message'))
            else:
                raise INXPOAPIException(row.get('Message'))

    assert data.OpCodeResult[2].get('OpCode') == 'T', \
        "We assume that the results are returned in order."

    login_ticket = data.OpCodeResult[2].ResultRow.LoginTicketKey
    return LOGIN_TICKET_URL.format(login_ticket=login_ticket)
