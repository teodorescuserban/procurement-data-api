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

## Examples

### Contract-notice examples

#### CSV contract notice

```
contract,title_en,title_fr,date_awarded,date_expires,value,supplier,supplier_city,supplier_region,buyer_en,buyer_fr,gsins,url_en,url_fr
21K01-022267/001/PQ,Office Furniture,Meubles de bureau,2013-04-29,2015-10-30,25000000.00,KRUEGER INTERNATIONAL INC ACTING THROUGH OEI,GREEN BAY,Wisconsin,Correctional Service of Canada,Service correctionnel du Canada,N7110,https://buyandsell.gc.ca/procurement-data/contract-history/21K01-022267-001-PQ,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/21K01-022267-001-PQ
```

#### JSON contract notice

```
{
  "url_en": "https://buyandsell.gc.ca/procurement-data/contract-history/21K01-022267-001-PQ",
  "gsins": [
    "N7110"
  ],
  "contract": "21K01-022267/001/PQ",
  "date_expires": "2015-10-30",
  "value": "25000000.00",
  "supplier_city": "GREEN BAY",
  "buyer_fr": "Service correctionnel du Canada",
  "buyer_en": "Correctional Service of Canada",
  "title_en": "Office Furniture",
  "supplier_region": "Wisconsin",
  "date_awarded": "2013-04-29",

  "supplier": "KRUEGER INTERNATIONAL INC ACTING THROUGH OEI",
  "title_fr": "Meubles de bureau"
}
```

### Tender-notice examples

### CSV tender notice

```
tender,title_en,title_fr,buyer_en,buyer_fr,gsins,regions_delivery,regions_opportunity,url_en,url_fr,date_closing
PW-$$FE-176-68065,Environmental Consultant for West Memorial Building (WMB) Asset Integrity Project (EH900-160791/A),Expert-Conseil en Environnement pour le projet d'intégrité des biens de l'Édifice commémoratif de l' (EH900-160791/A),Public Works and Government Services Canada,Travaux publics et Services gouvernementaux Canada,C219DA,ON,,https://buyandsell.gc.ca/procurement-data/tender-notice/PW-FE-176-68065,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-FE-176-68065,2015-11-16
```

### JSON tender notice

```
{
  "regions_delivery": [
    "ON"
  ],
  "title_en": "Environmental Consultant for West Memorial Building (WMB) Asset Integrity Project (EH900-160791/A)",
  "buyer_fr": "Travaux publics et Services gouvernementaux Canada",
  "buyer_en": "Public Works and Government Services Canada",
  "title_fr": "Expert-Conseil en Environnement pour le projet d'int\u00e9grit\u00e9 des biens de l'\u00c9difice comm\u00e9moratif de l' (EH900-160791/A)",
  "date_closing": "2015-11-16",
  "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-FE-176-68065",
  "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-FE-176-68065",
  "tender": "PW-$$FE-176-68065",
  "solicitation_number": "EH900-160791/A",
  "regions_opportunity": [],
  "gsins": [
    "C219DA"
  ]
}
```
