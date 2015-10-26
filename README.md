# Simple API for procurement data

_Started by David Megginson, 2015-10_

## Setup

**Note:** requires Python3.  This will not work with Python 2.7.

1. Create a new MySQL database (e.g. "bas").
2. Set up the database schema: ``mysql bas < sql/schema.sql``
3. Copy the ``config.py.TEMPLATE`` file to ``config.py`` and fill in your local database connection information.
4. Set up a Python virtualenv for the app: ``mkvirtualenv -p /usr/bin/python3 bas``
5. Install dependencies: ``python3 setup.py build``
6. Download [procurement data](https://buyandsell.gc.ca/procurement-data/csv/tender/active) from BuyAndSell.
7. Load the data into the database: ``python load_data.py tpsgc-pwgsc_ao-t_a.csv``

## Running (single thread)

```
python bas/api.py
```

## Usage

The extension after ``tender-notices`` selects the data type.  You can use ``tender-notices.csv`` for [Command-Separated Values](https://en.wikipedia.org/wiki/Comma-separated_values) output (suitable for opening with a spreadsheet application), or ``tender-notices.json`` for [JavaScript Object Notation](https://en.wikipedia.org/wiki/JSON) output (suitable for embedding in a web application).  By default, these returns all active tender notices, but you can filter results using the following GET parameters (all optional):

``gsins`` — a comma-separated list of GSIN-code prefixes to match, e.g. ``gsins=N7610,V204``.  These will match any GSIN codes that begin with those letters, e.g. _N7610AA_ or _V204B._  A tender notice needs to match only one of the GSIN codes.

``delivery`` — a comma-separated list of codes to match for the region of delivery, e.g. ``delivery=ON,QC,NCR``.  In addition to the two-letter codes for the 13 provinces and territories, some tender notices may include ``NCR`` for the national-capital region, ``CAN`` for Canada-wide, ``ABL`` for aboriginal lands, ``USA`` for the United States, ``MEX`` for Mexico, or ``INT`` for international.  Tender notices are not consistent, and may (for example) list ``CAN``, all of the province codes separately, or both to indicate a tender that applies to the whole country.

``opportunity`` — a comma-separated list of codes to match for the region of opportunity, e.g. ``opportunity=PE,NS,NB``.  The codes are the same as for the _delivery_ parameter.

## Examples

Find all tender notices that have a GSIN code starting with "N76" or "V2", and a delivery region of Ontario, Quebec, the National Capital Region, or Canada-wide.

### CSV output

**URL:** http://bas-api.megginson.com/tender-notices.csv?gsins=N76,V2&delivery=ON,QC,NCR,CAN

**Result:**

```
tender,title_en,title_fr,url_en,url_fr,gsins,regions_delivery,regions_opportunity
PW-$$ZL-102-25299,AIR CHARTER SERVICES (E60SQ-020001/B),SERVICES D'AFFRÈTEMENT AÉRIEN (E60SQ-020001/B),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-ZL-102-25299,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-ZL-102-25299,"V201A,V201B","NCR,ON,QC",
PW-$KIN-650-6679,AIRCRAFT RENTAL with Pilot(s) (W2037-150072/D),la location d'aéronefs avec pilote(s) (W2037-150072/D),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-KIN-650-6679,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-KIN-650-6679,V204IA,"NCR,ON,QC",
PW-13-00360795,Canada Post: Transportation Opportunities (Canada Post / Postes Canada),Postes Canada: Occasions de Transport du courrier (Canada Post / Postes Canada),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00360795,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00360795,V204B,CAN,CAN
PW-13-00538668,Printing Logbooks and Combined Forms for Fisheries and Oceans Canada (F5211-130006),Impression des journaux de bord et des formulaires combinés pour Pêches et Océans Canada (F5211-130006),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00538668,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00538668,"N7610AA,N7610D",CAN,CAN
PW-15-00700569,LEOPARD 2 - SPARE PARTS (GRK(W8486-162741/000/A)),LEOPARD 2 - PIECES DE RECHANGE (GRK(W8486-162741/000/A)),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-15-00700569,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-15-00700569,N7690,QC,INT
```

### JSON output

**URL:** http://example.org/tender-notices.json?gsins=N76,V2&delivery=ON,QC,NCR,CAN

**Result:**

```
[
  {
    "regions_delivery": [
      "CAN"
    ],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00360795",
    "title_en": "Canada Post: Transportation Opportunities (Canada Post / Postes Canada)",
    "title_fr": "Postes Canada: Occasions de Transport du courrier (Canada Post / Postes Canada)",
    "tender": "PW-13-00360795",
    "regions_opportunity": [
      "CAN"
    ],
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00360795",
    "gsins": [
      "V204B"
    ]
  },
  {
    "regions_delivery": [
      "CAN"
    ],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00538668",
    "title_en": "Printing Logbooks and Combined Forms for Fisheries and Oceans Canada (F5211-130006)",
    "title_fr": "Impression des journaux de bord et des formulaires combin\u00e9s pour P\u00eaches et Oc\u00e9ans Canada (F5211-130006)",
    "tender": "PW-13-00538668",
    "regions_opportunity": [
      "CAN"
    ],
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00538668",
    "gsins": [
      "N7610AA",
      "N7610D"
    ]
  },
  {
    "regions_delivery": [
      "QC"
    ],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-15-00700569",
    "title_en": "LEOPARD 2 - SPARE PARTS (GRK(W8486-162741/000/A))",
    "title_fr": "LEOPARD 2 - PIECES DE RECHANGE (GRK(W8486-162741/000/A))",
    "tender": "PW-15-00700569",
    "regions_opportunity": [
      "INT"
    ],
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-15-00700569",
    "gsins": [
      "N7690"
    ]
  }
]
```

## Coming soon ...

* Support for contract history and GSIN lookup (handles only tender notices right now) [#3](https://github.com/PWGSC-DEEN/procurement-data-api/issues/3) and  [#4](https://github.com/PWGSC-DEEN/procurement-data-api/issues/4)
* Output formats beyond JSON (CSV and XML).  [#5](https://github.com/PWGSC-DEEN/procurement-data-api/issues/5)
* Fuzzy lookup support: if there are no exact GSIN matches, look for something sort-of similar. [#6](https://github.com/PWGSC-DEEN/procurement-data-api/issues/6)
* Docker setup script (to build as a container).  [#7](https://github.com/PWGSC-DEEN/procurement-data-api/issues/7)

