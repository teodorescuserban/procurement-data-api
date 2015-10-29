#!/usr/bin/python3
# coding=utf8

import collections, csv, sys

        
if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8-sig') as input:
        contracts = ContractList(input)
        for contract in contracts:
            print(contract)
