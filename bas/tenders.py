#!/usr/bin/python3
# coding=utf8
"""Parse tender notices from BuyAndSell."""

import sys
import csv
import re
import collections
import pprint

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
    'Monde': 'INT',
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

class TenderList(object):
    """A list of tender notices."""

    def __init__(self, input):
        super().__init__()
        self.input = input
        self.reader = csv.DictReader(input)
        self.row = None

    def __iter__(self):
        return self

    def __next__(self):
        """Read the next tender."""
        # This is tricky, because the tenders appear on multiple rows

        if self.row is None:
            self.row = next(self.reader)
        
        tender = {}
        reference_number = self.row['reference_number']
        try:
            while self.row['reference_number'] == reference_number:
                # will always be true on first pass
                tender = self._parse(tender, self.row)
                self.row = next(self.reader)
            return tender
        except StopIteration:
            # Make sure we don't miss the last tender
            if tender:
                self.row = None
                return tender
            else:
                raise StopIteration

    @staticmethod
    def _parse(tender, row):
        """
        Import a single tender from a CSV row.
        @param row The CSV data row to load.
        """

        tender['reference-number'] = row['reference_number']
        tender['solicitation-number'] = row['solicitation_number']

        if row['language'] == 'English':
            tender['title_en'] = row['title']
            tender['description_en'] = row['description']
            tender['buyer_en'] = row['end_user_entity']
        else:
            tender['title_fr'] = row['title']
            tender['description_fr'] = row['description']
            tender['buyer_fr'] = row['end_user_entity']

        if not tender.get('date-closing'):
            tender['date-closing'] = TenderList._parse_date(row['date_closing'])

        if not tender.get('gsins'):
            tender['gsins'] = TenderList._parse_gsins(row['gsin'])

        if not tender.get('regions-delivery'):
            tender['regions-delivery'] = TenderList._parse_regions(row['region_delivery'])

        if not tender.get('regions-opportunity'):
            tender['regions-opportunity'] = TenderList._parse_regions(row['region_opportunity'])

        return tender

    @staticmethod
    def _parse_regions(s):
        """Parse comma-separated list of regions."""
        return set([REGION_MAP[region].upper() for region in re.split(r',\s*', s) if region and REGION_MAP[region]])

    @staticmethod
    def _parse_gsins(s):
        """Parse multiple GSINs from a single field."""

        # The CSV uses comma both as punctuation with a GSIN title and as
        # the field separator, so we can't simply do a split.
        gsins = []
        result = re.search(r'([A-Z][A-Z0-9]+):', s)
        while result:
            gsins.append(result.group(1).upper())
            s = s[result.end():]
            result = re.search(r'([A-Z][A-Z0-9]+):', s)
        return set(gsins)

    @staticmethod
    def _parse_date(s):
        result = re.match(r'^(2\d{3}-\d{2}-\d{2})\s*(\d{2}:\d{2})\s*(.+)$', s)
        if result:
            # Ignoring the time
            return result.group(1)
        else:
            raise Exception("Unparseable date: {}".format(s))

if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
        tenders = TenderList(input)
        for tender in tenders:
            pprint.pprint(tender)
