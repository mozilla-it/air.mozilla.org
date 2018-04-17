import random
import string

from django.test import TestCase

from .models import Event

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
