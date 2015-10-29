"""
Unit tests for the bas.tenders module
David Megginson
October 2015

License: Public Domain
"""

import unittest
from tests import resolve_file
from bas.tenders import TenderList

class TestTenderList(unittest.TestCase):

    # Expected values (some have changed from original)
    EXPECTED = {
        'reference-number': 'PW-$$ZT-009-27511',
        'solicitation-number': 'E60ZT-120001/E',
        'title_en': 'ProServices/ProServices (E60ZT-120001/E)',
        'title_fr': 'Services Pro (E60ZT-120001/E)',
        'gsins': {'D302A', 'R019BF'},
        'description_en': '<English description>',
        'description_fr': '<Description française>',
        'buyer_en': 'Public Works and Government Services Canada',
        'buyer_fr': 'Travaux publics et Services gouvernementaux Canada',
        'regions-delivery': {'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT', 'NCR'},
        'regions-opportunity': {'ON', 'QC'},
        'date-closing': '2016-12-30'
    }

    def setUp(self):
        self.maxDiff = None
        with open(resolve_file('files/tender-notices.csv'), 'r') as input:
            self.tenders = TenderList(input);
            self.tender = next(self.tenders)

    def test_tender(self):
        self.assertEqual(self.EXPECTED, self.tender)

