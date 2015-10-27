#!/bin/sh

echo "Downloading tender notices from BuyAndSell ..."
cd Inputs
rm -f tender-notices.csv tender-notices.csv.gz
wget -O tender-notices.csv 'https://buyandsell.gc.ca/procurement-data/csv/tender/active'

echo "Loading tender notices into database..."
cd ..
python load_data.py Inputs/tender-notices.csv


