#!/usr/bin/python3

import sys
import csv
import re
import pprint

def parse_gsins(s):
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

def parse_regions(s):
    """Parse comma-separated list of regions."""
    return [region for region in re.split(r',\s*', s) if region]

def parse_url(row):
    id = re.sub(r'[^A-Z0-9-]', '', row.get('reference_number'))
    return 'https://buyandsell.gc.ca/procurement-data/tender-notice/' + id

def parse_record(row):
    """Parse a record from a CSV row."""
    return {
        'title': row.get('title'),
        'gsins': parse_gsins(row.get('gsin')),
        'language': row.get('language'),
        'reference_number': row.get('reference_number'),
        'amendment_number': row.get('amendment_number'),
        'regions_opportunity': parse_regions(row.get('region_opportunity')),
        'regions_delivery': parse_regions(row.get('region_delivery')),
        'url': parse_url(row)
    }

def import_data(input):
    """Import the data from a CSV file."""
    reader = csv.DictReader(input)
    for row in reader:
        record = parse_record(row)
        pprint.pprint(record)

if sys.argv[1]:
    with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
        import_data(input)
else:
    import_data(sys.stdin)

