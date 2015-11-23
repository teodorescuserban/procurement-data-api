#!/bin/sh
########################################################################
# Download latest data from BAS and load into database.
########################################################################

echo "Downloading active tenders from BuyAndSell ..."
cd Inputs
curl -f 'https://buyandsell.gc.ca/procurement-data/csv/tender/active' > tenders.csv

echo "Loading active tenders into database ..."
cd ..
python3 load-tenders.py Inputs/tenders.csv

echo "Done."
exit
