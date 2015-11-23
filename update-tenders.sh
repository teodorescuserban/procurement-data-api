#!/bin/sh
########################################################################
# Download latest data from BAS and load into database.
########################################################################

echo "Downloading active tenders from BuyAndSell ..."
cd Inputs
curl -f#L --compressed 'https://buyandsell.gc.ca/procurement-data/csv/tender/active' -o tenders.csv

echo "Loading active tenders into database ..."
cd ..
python load-tenders.py Inputs/tenders.csv

echo "Done."
exit
