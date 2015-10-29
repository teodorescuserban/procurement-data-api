#/usr/bin/env python3
"""Load BAS CSV data into the database, replacing any old tables."""

import config
import sys
import bas.tenders

#
# SQL query constants
#

INSERT_TENDER_QUERY = ' '.join((
    'insert into Tenders (tender, solicitation_number, title_en, title_fr, buyer_en, buyer_fr, date_closing)',
    'values (%s, %s, %s, %s, %s, %s, %s)'
))

INSERT_FULLTEXT_QUERY = ' '.join((
    'insert into TenderSearch(tender, lemma, lang)',
    'values (%s, %s, %s)'
))

INSERT_GSIN_QUERY = ' '.join((
    'insert into TenderGSINMap (tender, gsin)',
    'values (%s, %s)',
    'on duplicate key update tender=tender'
))

INSERT_REGION_QUERY = ' '.join((
    'insert into TenderRegionMap (tender, region, rel)',
    'values (%s, %s, %s)',
    'on duplicate key update tender=tender'
))


#
# Load the tenders
#
with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
    tenders = bas.tenders.TenderList(input)
    connection = bas.connect(config)
    with connection.cursor() as cursor:

        cursor.execute('delete from Tenders')
        cursor.execute('delete from TenderSearch')

        for counter, tender in enumerate(tenders):

            if ((counter+1) % 100) == 0:
                print("{}...".format(counter+1))

            cursor.execute(INSERT_TENDER_QUERY, (
                tender['reference-number'],
                tender['solicitation-number'],
                tender['title_en'],
                tender['title_fr'],
                tender['buyer_en'],
                tender['buyer_fr'],
                tender['date-closing']
            ))

            cursor.execute(INSERT_FULLTEXT_QUERY, (
                tender['reference-number'],
                ' '.join((tender['title_en'], tender['description_en'])),
                'en'
            ))

            cursor.execute(INSERT_FULLTEXT_QUERY, (
                tender['reference-number'],
                ' '.join((tender['title_fr'], tender['description_fr'])),
                'fr'
            ))

            for gsin in tender['gsins']:
                cursor.execute(INSERT_GSIN_QUERY, (
                    tender['reference-number'], 
                    gsin
                ))

            for region in tender['regions-delivery']:
                cursor.execute(INSERT_REGION_QUERY, (
                    tender['reference-number'], 
                    region, 
                    'delivery'
                ))

            for region in tender['regions-opportunity']:
                cursor.execute(INSERT_REGION_QUERY, (
                    tender['reference-number'], 
                    region, 
                    'opportunity'
                ))

    connection.commit()
