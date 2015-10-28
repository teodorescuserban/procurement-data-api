#!/usr/bin/python3
# coding=utf8

import collections, csv, sys

class ContractList(object):
    """Iterable list of contract records from a CSV"""

    def __init__(self, input):
        super().__init__()
        self.input = input
        self.reader = csv.DictReader(input)

    def __iter__(self):
        return self

    def __next__(self):
        return self._parse(next(self.reader))

    def _parse(self, row):
        return {
            'contract': row.get('contract-number'),
            'title_en': row.get('gsin-description_en'),
            'title_fr': row.get('gsin-description_fr'),
            'date-awarded': row.get('award-date'),
            'date-expires': row.get('expiry-date'),
            'value': row.get('total-contract-value'),
            'supplier': row.get('supplier-operating-name') or row.get('supplier-legal-name'),
            'supplier-city': row.get('supplier-address-city'),
            'supplier-region': row.get('supplier-address-prov-state'),
            'buyer_en': row.get('end-user-entity_en'),
            'buyer_fr': row.get('end-user-entity_fr'),
            'gsin': row.get('gsin')
        }
        
if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
        contracts = ContractList(input)
        for contract in contracts:
            print(contract)
