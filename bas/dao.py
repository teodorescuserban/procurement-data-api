"""Data access."""

import bas
import config
import collections
import re


# Query template for tender searches
TENDER_QUERY_TEMPLATE = ' '.join((
    'select tender, solicitation_number,',
    'title_en, title_fr,',
    'buyer_en, buyer_fr,',
    'date_format(date_closing, "%Y-%m-%d") as date_closing,',
    'group_concat(distinct gsin separator ",") as gsins,',
    'group_concat(distinct region_delivery separator ",") as regions_delivery,',
    'group_concat(distinct region_opportunity separator ",") as regions_opportunity',
    'from TenderView',
    'left join TenderSearch using (tender)'
    'where {conditions}',
    'group by tender, title_en, title_fr',
    'order by date_closing',
    'limit 100'
))


# Query template for contract searches
CONTRACT_QUERY_TEMPLATE = ' '.join((
    'select contract, title_en, title_fr,'
    'date_format(date_awarded, "%Y-%m-%d") as date_awarded,'
    'date_format(date_expires, "%Y-%m-%d") as date_expires,'
    'value, supplier, supplier_city, supplier_region,',
    'buyer_en, buyer_fr, gsin',
    'from Contracts',
    'where {conditions}',
    'order by date_expires',
    'limit 100'
))


def esc(s):
    """SQL escape a string."""
    return bas.connect(config).escape_string(s)


def sql_row_to_dict(cursor, row):
    """Convert a row of a SQL result into a Python dict."""
    data = {}
    for i, value in enumerate(row):
        name = cursor.description[i][0]
        if name in ('gsins', 'regions_opportunity', 'regions_delivery'):
            if value:
                value = value.split(',')
            else:
                value = ()
        data[name] = value
    return data

def search_tenders(gsins=[], delivery=[], opportunity=[], keywords=[]):
    """Search for matching tenders."""

    # Make the SQL condition fragments (a bit of ugly here)
    conditions = []
    conditions.append(' or '.join(["gsin like '{}%'".format(esc(gsin)) for gsin in gsins if gsin]))
    conditions.append(' or '.join(["region_delivery='{}'".format(esc(region)) for region in delivery if region]))
    conditions.append(' or '.join(["region_opportunity='{}'".format(esc(region)) for region in opportunity if region]))
    conditions.append(' or '.join(["tender in (select tender from TenderSearch where match(lemma) against('{}'))".format(esc(keyword)) for keyword in keywords if keyword]))
    condition_fragment = ' and '.join(["({})".format(condition) for condition in conditions if condition])
    if not condition_fragment:
        condition_fragment = 'true';

    # Make the SQL query string
    query = TENDER_QUERY_TEMPLATE.format(conditions=condition_fragment)

    # Post-processing for each result row
    def post_tender(cursor, row):
        data = sql_row_to_dict(cursor, row)
        # Generate URLs to BAS
        id = re.sub(r'[^A-Z0-9-]', '', data['tender'])
        data['url_en'] = 'https://buyandsell.gc.ca/procurement-data/tender-notice/{}'.format(id)
        data['url_fr'] = 'https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/{}'.format(id)
        return data

    # Execute the query
    connection = bas.connect(config)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return [post_tender(cursor, row) for row in result]


def search_contracts(gsins=[], keywords=[]):
    """Search for matching contracts."""

    # Make the SQL condition fragments (ugly, again)
    conditions = []
    conditions.append(' or '.join(["gsin like '{}%'".format(esc(gsin)) for gsin in gsins if gsin]))
    conditions.append(' or '.join(["contract in (select contract from ContractSearch where match(lemma) against('{}'))".format(esc(keyword)) for keyword in keywords if keyword]))
    condition_fragment = ' and '.join(["({})".format(condition) for condition in conditions if condition])
    if not condition_fragment:
        condition_fragment = 'true';

    # Make the SQL query string
    query = CONTRACT_QUERY_TEMPLATE.format(conditions=condition_fragment)

    # Post-processing for each result row
    def post_contract(cursor, row):
        data = sql_row_to_dict(cursor, row)
        data['gsins'] = [data['gsin']]
        del data['gsin']
        id = re.sub(r'[^A-Z0-9-]', '-', data['contract'])
        data['url_en'] = 'https://buyandsell.gc.ca/procurement-data/contract-history/{}'.format(id)
        data['url_fr'] = 'https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/{}'.format(id)
        return data

    # Execute the query
    connection = bas.connect(config)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return [post_contract(cursor, row) for row in result]
        
