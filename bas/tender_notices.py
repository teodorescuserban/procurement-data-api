#!/usr/bin/python3

import sys
import csv
import re
import collections

REGION_MAP = {
    'Aboriginal Lands': 'ABL',
    'Alberta': 'AB',
    'British Columbia': 'BC',
    'Canada': 'CAN',
    'Colombie-Britannique': 'BC',
    'États-Unis': 'USA',
    'Foreign': 'X-INT',
    'Île-du-Prince-Édouard': 'PE',
    'Internationale': 'INT',
    'Manitoba': 'MB',
    'Mexico': 'MEX',
    'Mexique': 'MEX',
    'Monde': 'GLB',
    'National Capital Region': 'NCR',
    'New Brunswick': 'NB',
    'Newfoundland and Labrador': 'NL',
    'Non spécifiée': None,
    'Northwest Territories': 'NT',
    'Nouveau-Brunswick': 'NB',
    'Nouvelle-Écosse': 'NS',
    'Nova Scotia': 'NS',
    'Nunavut': 'NU',
    'Ontario': 'ON',
    'Prince Edward Island': 'PE',
    'Quebec': 'QC',
    'Québec': 'QC',
    'Région de la capitale nationale': 'NCR',
    'Saskatchewan': 'SK',
    'Terre-Neuve-et-Labrador': 'NL',
    'Terres autochtones': 'ABL',
    'Territoires du Nord-Ouest': 'NT',
    'United States': 'USA',
    'Unspecified': None,
    'World': 'INT',
    'Yukon': 'YT'
}

class TenderNoticeList(collections.UserDict):
    """A list of tender notices."""

    def __init__(self):
        super().__init__()

    def load_notice(self, row):
        """
        Import a single notice from a CSV row.
        @param row The CSV data row to load.
        """
        refno = row.get('reference_number').upper()
        if not refno:
            raise Exception("No reference number provided: " + str(row))
        notice = self.data.get(refno)
        if notice:
            notice.load(row)
        else:
            notice = TenderNotice(row)
            self.data[refno] = notice

    @staticmethod
    def load(source):
        """
        Load a list of notices from CSV.
        @param source A filename or input stream for a CSV file.
        @return a TenderNoticeList object
        """
        print("Source is {}".format(source))
        if hasattr(source, 'read'):
            return TenderNoticeList._load(source)
        else:
            with open(source, 'r', encoding='utf-8-sig') as input:
                return TenderNoticeList._load(input)

    @staticmethod
    def _load(input):
        """Internal load method."""
        notices = TenderNoticeList()
        reader = csv.DictReader(input)
        for row in reader:
            notices.load_notice(row)
        return notices

    
class TenderNotice(object):
    """A single tender notice"""

    def __init__(self, row=None):
        self.gsins = set()
        self.regions_delivery = set()
        self.regions_opportunity = set()
        if row:
            self.load(row)

    def load(self, row):
        self.reference_number = row['reference_number']
        if row['language'] == 'English':
            self.title_en = row['title']
        else:
            self.title_fr = row['title']

        self.urls = self._parse_urls(row)

        gsins = self._parse_gsins(row['gsin'])
        self.gsins = self.gsins.union(gsins)

        regions = self._parse_regions(row['region_delivery'])
        self.regions_delivery = self.regions_opportunity.union(regions)

        regions = self._parse_regions(row['region_opportunity'])
        self.regions_opportunity = self.regions_opportunity.union(regions)

    def __str__(self):
        return "<Tender notice: {} {}>".format(self.reference_number, self.title_en)

    def _parse_regions(self, s):
        """Parse comma-separated list of regions."""
        return [REGION_MAP[region].upper() for region in re.split(r',\s*', s) if region and REGION_MAP[region]]

    def _parse_gsins(self, s):
        """Parse multiple GSINs from a single field."""

        # The CSV uses comma both as punctuation with a GSIN title and as
        # the field separator, so we can't simply do a split.
        gsins = []
        result = re.search(r'([A-Z][A-Z0-9]+):', s)
        while result:
            gsins.append(result.group(1).upper())
            s = s[result.end():]
            result = re.search(r'([A-Z][A-Z0-9]+):', s)
        return gsins

    def _parse_urls(self, row):
        """Parse and construct BuyAndSell URLs."""
        id = re.sub(r'[^A-Z0-9-]', '', row.get('reference_number'))
        return {
            'en': 'https://buyandsell.gc.ca/procurement-data/tender-notice/' + id,
            'fr': 'https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/' + id
        }

    @staticmethod
    def load_data(input):
        """Import the data from a CSV file."""
        notices = TenderNoticeList()
        reader = csv.DictReader(input)
        for row in reader:
            notices.load_notice(row)
        return notices

