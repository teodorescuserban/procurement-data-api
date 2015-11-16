# Procurement API data formats

_Started by David Megginson, 2015-11_

The procurement API can return data in CSV or JSON format, using the following fields.  In CSV lists (such as GSINs) are comma-separated tokens; in JSON, they are proper lists.

## Common fields

| Field    | Description                                                       |
|----------|-------------------------------------------------------------------|
| title_en | Contract or tender title (English)                                |
| title_fr | Contract or tender title (French)                                 |
| buyer_en | Buyer department name (English)                                   |
| buyer_fr | Buyer department name (French)                                    |
| url_en   | Contract or tender link on BuyAndSell (English)                   |
| url_fr   | Contract or tender link on BuyAndSell (French)                    |
| gsins    | List of GSIN classification codes (always one code for contracts) |

## Tender data only

| Field               | Description                                                      |
|---------------------|------------------------------------------------------------------|
| tender              | Unique identifier for the tender notice                          |
| solicitation_number | Solicitation number associated with the tender                   |
| date_closing        | Closing date in YYYY-MM-DD format (time not included)            |
| regions_opportunity | List of region codes where the supplier may be located           |
| regions_delivery    | List of region codes where the good or service will be delivered |

## Contract data only

| Field           | Description                                                                       |
| ----------------|-----------------------------------------------------------------------------------|
| contract        | Unique identifier for the contract notice                                         |
| date_awarded    | Date when the contract was awarded, in YYYY-MM-DD format                          |
| date_expires    | Date when the contract finishes, in YYYY-MM-DD format                             |
| value           | The value of the contract (free-form string)                                      |
| supplier        | The supplier's name, in whatever language the supplier chose                      |
| supplier_city   | The city where the supplier is based                                              |
| supplier_region | The region where the supplier is based (see the region lists for a tender notice) |
