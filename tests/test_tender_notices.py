"""
Unit tests for the bas.tender_notices module
David Megginson
October 2015

License: Public Domain
"""

import unittest
from tests import resolve_file
from bas.tender_notices import TenderNoticeList

class TestTenderNotice(unittest.TestCase):

    # Expected values (some have changed from original)
    REFNO = 'PW-$$ZT-009-27511'
    TITLE_EN = 'ProServices/ProServices (E60ZT-120001/E)'
    TITLE_FR = 'Services Pro (E60ZT-120001/E)'
    GSINS = {'D302A', 'R019BF'}
    DESCRIPTION_EN = '<English description>'
    DESCRIPTION_FR = '<Description française>'
    REGIONS_DELIVERY = {'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT', 'NCR'}
    REGIONS_OPPORTUNITY = {'ON', 'QC'}

    def setUp(self):
        self.maxDiff = None
        with open(resolve_file('files/tender-notices.csv'), 'r') as input:
            self.notices = TenderNoticeList.load(input);
        self.notice = self.notices.get(self.REFNO)

    def test_tender(self):
        self.assertTrue(self.notice)
        self.assertFalse(self.notices.get('XXX'))

    def test_refno(self):
        self.assertEqual(self.REFNO, self.notice.reference_number)

    def test_title(self):
        self.assertEqual(self.TITLE_EN, self.notice.title_en)
        self.assertEqual(self.TITLE_FR, self.notice.title_fr)

    def test_description(self):
        self.assertEqual(self.DESCRIPTION_EN, self.notice.description_en)
        self.assertEqual(self.DESCRIPTION_FR, self.notice.description_fr)

    def test_gsins(self):
        self.assertEqual(self.GSINS, self.notice.gsins)

    def test_regions(self):
        self.assertEqual(self.REGIONS_DELIVERY, self.notice.regions_delivery)
        self.assertEqual(self.REGIONS_OPPORTUNITY, self.notice.regions_opportunity)

