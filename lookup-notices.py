#!/usr/bin/python3

import bas
import config
import sys

SEARCH_QUERY = ' '.join((
    'select tender, title_en, title_fr,',
    'group_concat(distinct gsin separator ",") as gsins,',
    'group_concat(distinct region_delivery separator ",") as regions_delivery,',
    'group_concat(distinct region_opportunity separator ",") as regions_opportunity',
    'from TenderView',
    'where gsin like %s',
    'group by tender, title_en, title_fr'
))

connection = bas.connect(config)

gsin = sys.argv[1]

with connection.cursor() as cursor:
    cursor.execute(SEARCH_QUERY, (gsin + '%'))
    result=cursor.fetchall()
    for row in result:
        print(row)
