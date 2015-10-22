"""Data access."""

import bas
import config

SEARCH_QUERY = ' '.join((
    'select tender, title_en, title_fr,',
    'group_concat(distinct gsin separator ",") as gsins,',
    'group_concat(distinct region_delivery separator ",") as regions_delivery,',
    'group_concat(distinct region_opportunity separator ",") as regions_opportunity',
    'from TenderView',
    'where gsin like %s',
    'group by tender, title_en, title_fr'
))

def fix_row(cursor, row):
    data = {}
    for i, value in enumerate(row):
        name = cursor.description[i][0]
        if name in ('gsins', 'regions_opportunity', 'regions_delivery'):
            value = value.split(',')
        data[name] = value
    return data

def search(gsin):
    connection = bas.connect(config)
    with connection.cursor() as cursor:
        cursor.execute(SEARCH_QUERY, (gsin + '%'))
        result = cursor.fetchall()
        return [fix_row(cursor, row) for row in result]

