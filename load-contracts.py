#/usr/bin/env python3
"""Load BAS CSV data into the database, replacing any old tables."""

import config
import sys
import datetime

import bas
from bas.input import ContractList

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

INSERT_FULLTEXT_QUERY = ' '.join((
    'insert into ContractSearch(contract, lemma, lang)',
    'values (%s, %s, %s)'
))

#
# Load the contracts
#
with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
    contracts = ContractList(input)
    connection = bas.connect(config)
    with connection.cursor() as cursor:
        today = str(datetime.date.today())
        cursor.execute('delete from Contracts')
        cursor.execute('delete from ContractSearch')
        for counter, contract in enumerate(contracts):
            if (counter + 1) % 5000 == 0:
                print("{}...".format(counter+1))
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
                result = cursor.execute(INSERT_FULLTEXT_QUERY, (
                    contract['contract'],
                    ' '.join((
                        contract['title_en'],
                        contract['supplier'],
                        contract['supplier-city'],
                        contract['supplier-region'],
                        contract['buyer_en']
                    )),
                    'en'
                ));
                result = cursor.execute(INSERT_FULLTEXT_QUERY, (
                    contract['contract'],
                    ' '.join((
                        contract['title_fr'],
                        contract['supplier'],
                        contract['supplier-city'],
                        contract['supplier-region'],
                        contract['buyer_fr']
                    )),
                    'fr'
                ));
    connection.commit()
