#!/usr/bin/python3

import sys
import csv
import re
import pprint

class TenderNotice(object):

    def __init__(self, row=None):
        self.gsins = set()
        self.regions_delivery = set()
        self.regions_opportunity = set()
        if row:
            self.merge(row)

    def merge(self, row):
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

    def _parse_regions(self, s):
        """Parse comma-separated list of regions."""
        return [region for region in re.split(r',\s*', s) if region]

    def _parse_gsins(self, s):
        """Parse multiple GSINs from a single field."""

        # The CSV uses comma both as punctuation with a GSIN title and as
        # the field separator, so we can't simply do a split.
        gsins = []
        result = re.search(r'([A-Z][A-Z0-9]+):', s)
        while result:
            gsins.append(result.group(1))
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

def import_data(input):
    """Import the data from a CSV file."""
    reader = csv.DictReader(input)
    for row in reader:
        notice = TenderNotice(row)
        print(notice)

if sys.argv[1]:
    with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
        import_data(input)
else:
    import_data(sys.stdin)

