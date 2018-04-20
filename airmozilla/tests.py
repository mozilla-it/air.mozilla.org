import random
import string

from django.test import TestCase, override_settings
from django.conf import settings

from .models import Event
from .inxpo import (
    retrieve_events, retrieve_privacy_strategy, retrieve_event_time_range,
    INXPOAPIException, EventNotFoundException, setup_constants,
    get_anonymous_login_url_for_event
)


unicode_alphabet = [
    chr(code_point) for code_point in range(0, 0x10ffff + 1)
    # Exclude surrogate code points, they are not allowed to be encoded in utf8.
    if not (0xd800 <= code_point <= 0xdfff)
]


def get_random_unicode(length):
    return ''.join(random.choice(unicode_alphabet) for i in range(length))


def get_random_ascii(length):
    return ''.join(random.choice(string.printable) for i in range(length))


class TestSearch(TestCase):
    def test_fuzz_process_query_unicode(self):
        """This just tests that our process_query can't cause a syntax error."""

        for i in range(1000):
            s = get_random_unicode(random.randrange(0, 500))
            try:
                list(Event.objects.search(s))
            except:
                print(repr(s))
                raise

        list(Event.objects.search('\x00'))

    def test_fuzz_process_query_ascii(self):
        for i in range(1000):
            s = get_random_ascii(random.randrange(0, 500))
            try:
                list(Event.objects.search(s))
            except:
                print(repr(s))
                raise


def override_inxpo(params):
    def inner(fn):
        @override_settings(INXPO_PARAMETERS=params)
        def test_fn(*args, **kwargs):
            setup_constants()
            return fn(*args, **kwargs)
        return test_fn
    return inner


class TestINXPO(TestCase):
    def setUp(self):
        setup_constants()

    def test_time_range_event_doesnt_exist(self):
        with self.assertRaises(EventNotFoundException):
            retrieve_event_time_range(102938109283)

    @override_inxpo({**settings.INXPO_PARAMETERS, 'SHOW_KEY': 123})
    def test_invalid_show_key(self):
        with self.assertRaisesMessage(INXPOAPIException, 'Invalid Show Key Specified!'):
            retrieve_events()

        with self.assertRaisesMessage(INXPOAPIException, 'Invalid Show Key Specified!'):
            retrieve_privacy_strategy()

        with self.assertRaisesMessage(INXPOAPIException, 'Invalid Show Key Specified!'):
            retrieve_event_time_range(246640)

    @override_inxpo({**settings.INXPO_PARAMETERS, 'AUTH_CODE': 'foo'})
    def test_invalid_auth(self):
        with self.assertRaisesMessage(INXPOAPIException, 'Invalid API Credentials Supplied!'):
            retrieve_events()

        with self.assertRaisesMessage(INXPOAPIException, 'Invalid API Credentials Supplied!'):
            retrieve_privacy_strategy()

        with self.assertRaisesMessage(INXPOAPIException, 'Invalid API Credentials Supplied!'):
            retrieve_event_time_range(246640)

        with self.assertRaisesMessage(INXPOAPIException, 'Invalid API Credentials Supplied!'):
            get_anonymous_login_url_for_event(246640)

    def test_login_url_event_doesnt_exist(self):
        with self.assertRaises(EventNotFoundException):
            get_anonymous_login_url_for_event(102938109283)

        with self.assertRaises(EventNotFoundException):
            get_anonymous_login_url_for_event(0)

    def test_success(self):
        retrieve_privacy_strategy()
        events = retrieve_events()
        retrieve_event_time_range(events[0].EventKey)
        assert get_anonymous_login_url_for_event(events[0].EventKey).startswith('http')
