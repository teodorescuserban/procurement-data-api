"""Data access."""

import bas
import config
import collections
import re

SEARCH_QUERY_TEMPLATE = ' '.join((
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
    'group by tender, title_en, title_fr'
))

CONTRACT_QUERY_TEMPLATE = ' '.join((
    'select contract, title_en, title_fr,'
    'date_format(date_awarded, "%Y-%m-%d") as date_awarded,'
    'date_format(date_expires, "%Y-%m-%d") as date_expires,'
    'value, supplier, supplier_city, supplier_region,',
    'buyer_en, buyer_fr, gsin',
    'from Contracts',
    'where {conditions}'
))

def esc(s):
    return bas.connect(config).escape_string(s)

def fix_row(cursor, row):
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

def post_tender(cursor, row):
    data = fix_row(cursor, row)
    # Generate URLs to BAS
    id = re.sub(r'[^A-Z0-9-]', '', data['tender'])
    data['url_en'] = 'https://buyandsell.gc.ca/procurement-data/tender-notice/{}'.format(id)
    data['url_fr'] = 'https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/{}'.format(id)
    return data

def search(gsins=[], delivery=[], opportunity=[], keywords=[]):

    connection = bas.connect(config)

    conditions = []
    conditions.append(' or '.join(["gsin like '{}%'".format(esc(gsin)) for gsin in gsins if gsin]))
    conditions.append(' or '.join(["region_delivery='{}'".format(esc(region)) for region in delivery if region]))
    conditions.append(' or '.join(["region_opportunity='{}'".format(esc(region)) for region in opportunity if region]))
    conditions.append(' or '.join(["tender in (select tender from TenderSearch where match(lemma) against('{}'))".format(esc(keyword)) for keyword in keywords if keyword]))
    
    condition_fragment = ' and '.join(["({})".format(condition) for condition in conditions if condition])
    if not condition_fragment:
        condition_fragment = 'true';

    query = SEARCH_QUERY_TEMPLATE.format(conditions=condition_fragment)

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return [post_tender(cursor, row) for row in result]

def search_contracts(gsins=[], keywords=[]):

    connection = bas.connect(config)

    conditions = []
    conditions.append(' or '.join(["gsin like '{}%'".format(esc(gsin)) for gsin in gsins if gsin]))
    conditions.append(' or '.join(["contract in (select contract from ContractSearch where match(lemma) against('{}'))".format(esc(keyword)) for keyword in keywords if keyword]))
    
    condition_fragment = ' and '.join(["({})".format(condition) for condition in conditions if condition])
    if not condition_fragment:
        condition_fragment = 'true';

    query = CONTRACT_QUERY_TEMPLATE.format(conditions=condition_fragment)

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return [fix_row(cursor, row) for row in result]
        
