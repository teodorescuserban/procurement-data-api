"""Data access."""

import bas
import config
import collections
import re

SEARCH_QUERY_TEMPLATE = ' '.join((
    'select tender, title_en, title_fr,',
    'group_concat(distinct gsin separator ",") as gsins,',
    'group_concat(distinct region_delivery separator ",") as regions_delivery,',
    'group_concat(distinct region_opportunity separator ",") as regions_opportunity',
    'from TenderView',
    'where {conditions}',
    'group by tender, title_en, title_fr'
))

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
    # Generate URLs to BAS
    id = re.sub(r'[^A-Z0-9-]', '', data['tender'])
    data['url_en'] = 'https://buyandsell.gc.ca/procurement-data/tender-notice/{}'.format(id)
    data['url_fr'] = 'https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/{}'.format(id)
    return data

def search(gsins=[], delivery=[], opportunity=[]):

    connection = bas.connect(config)

    def esc(s):
        return connection.escape_string(s)

    conditions = []
    conditions.append(' or '.join(["gsin like '{}%'".format(esc(gsin)) for gsin in gsins if gsin]))
    conditions.append(' or '.join(["region_delivery='{}'".format(esc(region)) for region in delivery if region]))
    conditions.append(' or '.join(["region_opportunity='{}'".format(esc(region)) for region in opportunity if region]))

    condition_fragment = ' and '.join(["({})".format(condition) for condition in conditions if condition])
    if not condition_fragment:
        condition_fragment = 'true';

    query = SEARCH_QUERY_TEMPLATE.format(conditions=condition_fragment)

    print(query)

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return [fix_row(cursor, row) for row in result]

