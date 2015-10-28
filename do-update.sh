#!/bin/sh
########################################################################
# Download latest data from BAS and load into database.
########################################################################

echo "Downloading active tenders from BuyAndSell ..."
cd Inputs
rm -f tenders.csv
wget -q -O tenders.csv 'https://buyandsell.gc.ca/procurement-data/csv/tender/active'

echo "Loading active tenders into database ..."
cd ..
python load-tenders.py Inputs/tenders.csv

echo "Downloading all contracts from BuyAndSell ..."
cd Inputs
rm -f contracts.csv
wget -q -O contracts.csv 'https://buyandsell.gc.ca/cds/public/contracts/tpsgc-pwgsc_co-ch_tous-all.csv'

echo "Loading active tenders into database (will take a while) ..."
cd ..
python load-contracts.py Inputs/contracts.csv

echo "Done."
exit
