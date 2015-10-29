"""
Output functions

Generators to produce CSV rows.

Started 2015-10 by David Megginson
"""

import csv
import io
import json


# Headers for the tenders CSV
# (column names in the SQL)
TENDER_CSV_HEADERS = (
    'tender',
    'title_en',
    'title_fr',
    'buyer_en',
    'buyer_fr',
    'gsins',
    'regions_delivery',
    'regions_opportunity',
    'url_en',
    'url_fr',
    'date_closing'
)


# Headers for the contracts CSV
# (column names in the SQL)
CONTRACT_CSV_HEADERS = (
    'contract',
    'title_en',
    'title_fr',
    'date_awarded',
    'date_expires',
    'value',
    'supplier',
    'supplier_city',
    'supplier_region',
    'buyer_en',
    'buyer_fr',
    'gsins',
    'url_en',
    'url_fr'
)


def gen_json(records):
    """
    Generate JSON output for any data type.
    @param records a sequence of data records.
    @return generator for JSON output, line by line.
    """
    yield json.dumps(records, indent=2)


def gen_tenders_csv(tenders):
    """
    Generate CSV for tenders.
    @param tenders a sequence of tender records.
    @return generator for CSV tender output, line by line.
    """
    for row in _gen_csv(tenders, TENDER_CSV_HEADERS):
        yield row


def gen_contracts_csv(contracts):
    """
    Generate CSV for contracts.
    @param contracts a sequence of contract records.
    @return generator for CSV contract output, line by line.
    """
    for row in _gen_csv(contracts, CONTRACT_CSV_HEADERS):
        yield row


def _gen_csv(records, headers):
    """
    Generate generic CSV, line by line.
    @param records a list of data records.
    @param headers a sequence of header keys for each record.
    @return generator for CSV output, line by line.
    """
    yield(_serialise_csv_row(headers))
    for record in records:
        yield(_serialise_csv_row([_serialise_csv_value(record[header]) for header in headers]))


def _serialise_csv_value(value):
    """
    Serialise a value for CSV.
    @param value an atomic value or a sequence.
    @return the input value if atomic, or the sequence separated by commas.
    """
    if isinstance(value, str):
        return value
    else:
        return ','.join(value)


def _serialise_csv_row(row):
    """
    Render a row of values as CSV.
    @param row a sequence of string values.
    @return the sequence rendered as CSV, with escaping.
    """
    with io.StringIO() as output:
        writer = csv.writer(output)
        writer.writerow(row)
        return output.getvalue()

# end
