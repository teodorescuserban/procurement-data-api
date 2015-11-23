#!/bin/sh
########################################################################
# Download latest data from BAS and load into database.
########################################################################

echo "Downloading all contracts from BuyAndSell ..."
cd Inputs
curl -f 'https://buyandsell.gc.ca/cds/public/contracts/tpsgc-pwgsc_co-ch_tous-all.csv' > contracts.csv

echo "Loading active contracts into database (will take a while) ..."
cd ..
python3 load-contracts.py Inputs/contracts.csv

echo "Done."
exit
