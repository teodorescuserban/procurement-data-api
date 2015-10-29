#!/bin/sh
########################################################################
# Download latest data from BAS and load into database.
########################################################################

echo "Downloading all contracts from BuyAndSell ..."
cd Inputs
rm -f contracts.csv
wget -q -O contracts.csv 'https://buyandsell.gc.ca/cds/public/contracts/tpsgc-pwgsc_co-ch_tous-all.csv'

echo "Loading active contracts into database (will take a while) ..."
cd ..
python load-contracts.py Inputs/contracts.csv

echo "Done."
exit
