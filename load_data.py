#/usr/bin/env python3
"""Load BAS CSV data into the database, replacing any old tables."""

import config
import sys
import bas

#
# SQL query constants
#

INSERT_TENDER_QUERY = ' '.join((
    'insert into Tenders (tender, title_en, title_fr)',
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
# Load the notices
#
if sys.argv[1]:
    notices = bas.load_tenders(sys.argv[1])
else:
    notices = bas.load_tenders(sys.stdin)

#
# Open the database connection
#
connection = bas.connect(config)

#
# Load the notices into the database
#
with connection.cursor() as cursor:

    cursor.execute('delete from Tenders')
    
    for refno in notices:
        notice = notices.get(refno)

        result = cursor.execute(INSERT_TENDER_QUERY, (refno, notice.title_en, notice.title_fr))

        for gsin in notice.gsins:
            result = cursor.execute(INSERT_GSIN_QUERY, (refno, gsin))

        for region in notice.regions_delivery:
            result = cursor.execute(INSERT_REGION_QUERY, (refno, region, 'delivery'))

        for region in notice.regions_opportunity:
            result = cursor.execute(INSERT_REGION_QUERY, (refno, region, 'opportunity'))


connection.commit()
