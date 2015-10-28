#/usr/bin/env python3
"""Load BAS CSV data into the database, replacing any old tables."""

import config
import sys
import bas.contracts
import datetime

#
# SQL query constants
#

INSERT_CONTRACT_QUERY = ' '.join((
    'insert into Contracts',
    '(contract, title_en, title_fr, date_awarded, date_expires, value, supplier, supplier_city, supplier_region, buyer_en, buyer_fr, gsin)',
    'values',
    '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
    'on duplicate key update',
    'title_en = values(title_en),',
    'title_fr = values(title_fr),',
    'date_awarded = values(date_awarded),',
    'value = values(value),',
    'supplier = values(supplier),',
    'supplier_city = values(supplier_city),',
    'supplier_region = values(supplier_region),',
    'buyer_en = values(buyer_en),',
    'buyer_fr = values(buyer_fr),',
    'gsin = values(gsin)'
))

#
# Load the contracts
#
with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
    contracts = bas.contracts.ContractList(input)
    connection = bas.connect(config)
    with connection.cursor() as cursor:
        today = str(datetime.date.today())
        cursor.execute('delete from Contracts')
        for contract in contracts:
            if contract['date-expires'] > today:
                result = cursor.execute(INSERT_CONTRACT_QUERY, (
                    contract['contract'],
                    contract['title_en'],
                    contract['title_fr'],
                    contract['date-awarded'],
                    contract['date-expires'],
                    contract['value'],
                    contract['supplier'],
                    contract['supplier-city'],
                    contract['supplier-region'],
                    contract['buyer_en'],
                    contract['buyer_fr'],
                    contract['gsin']))
    connection.commit()
