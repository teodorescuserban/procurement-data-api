# Simple API for procurement data

_Started by David Megginson, 2015-10_


## Purpose

Allow applications to look up active Government of Canada tenders and contracts that may be of interest to a business.


## Setup

**Note:** requires Python3.  This will not work with Python 2.7.

1. Create a new MySQL database (e.g. "bas").
2. Set up the database schema: ``mysql bas < sql/schema.sql``
3. Copy the ``config.py.TEMPLATE`` file to ``config.py`` and fill in your local database connection information.
4. Set up a Python virtualenv for the app: ``mkvirtualenv -p /usr/bin/python3 bas``
5. Install dependencies: ``python3 setup.py build``
6. Download the data and load it into the database: ``sh do-update.sh``


## Running (single thread)

```
python bas/api.py
```


## Usage

The two main paths are ``/tenders`` and ``/contracts``, followed by a file-type extension:

* ``/tenders.json`` — return up to 100 matching active tenders in JSON format.
* ``/tenders.csv`` — return up to 100 matching active tenders in CSV format.
* ``/contracts.json`` — return up to 100 matching active contracts in JSON format.
* ``/contracts.csv`` — return up to 100 matching active contracts in CSV format.

The results are always sorted by date (closing date for a tender, expiry date for a contract).  You can refine them using the following GET parameters:

* **gsins** — specify a comma-separated list of GSIN prefixes to match, e.g. ``gsins=N7610,V204``. These will match any GSIN codes that begin with those letters, e.g. _N7610AA_ or _V204B._

* **keywords`** — a comma-separated list of keywords or phrases to search in both the title and (for a tender) description, e.g. ``keywords=drupal``.  The API will look for the keywords in both English and French text.

* **delivery** (tenders only) — a comma-separated list of codes to match for the region of delivery, e.g. ``delivery=ON,QC,NCR``.  In addition to the two-letter codes for the 13 provinces and territories, some tender notices may include ``NCR`` for the national-capital region, ``CAN`` for Canada-wide, ``ABL`` for aboriginal lands, ``USA`` for the United States, ``MEX`` for Mexico, or ``INT`` for international.  Tender notices are not consistent, and may (for example) list ``CAN``, all of the province codes separately, or both to indicate a tender that applies to the whole country.

* **opportunity** (tenders only) — a comma-separated list of codes to match for the region of opportunity, e.g. ``opportunity=PE,NS,NB``.  The codes are the same as for the _delivery_ parameter.


## Examples

Find all tender notices that have a GSIN code starting with "N76" or "V2", and a delivery region of Ontario, Quebec, the National Capital Region, or Canada-wide.


### CSV output

**URL:** http://bas-api.megginson.com/tenders.csv?gsins=N76,V2&delivery=ON,QC,NCR,CAN

**Result:**

```
tender,title_en,title_fr,url_en,url_fr,gsins,regions_delivery,regions_opportunity
PW-$$ZL-102-25299,AIR CHARTER SERVICES (E60SQ-020001/B),SERVICES D'AFFRÈTEMENT AÉRIEN (E60SQ-020001/B),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-ZL-102-25299,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-ZL-102-25299,"V201A,V201B","NCR,ON,QC",
PW-$KIN-650-6679,AIRCRAFT RENTAL with Pilot(s) (W2037-150072/D),la location d'aéronefs avec pilote(s) (W2037-150072/D),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-KIN-650-6679,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-KIN-650-6679,V204IA,"NCR,ON,QC",
PW-13-00360795,Canada Post: Transportation Opportunities (Canada Post / Postes Canada),Postes Canada: Occasions de Transport du courrier (Canada Post / Postes Canada),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00360795,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00360795,V204B,CAN,CAN
PW-13-00538668,Printing Logbooks and Combined Forms for Fisheries and Oceans Canada (F5211-130006),Impression des journaux de bord et des formulaires combinés pour Pêches et Océans Canada (F5211-130006),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00538668,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00538668,"N7610AA,N7610D",CAN,CAN
PW-15-00700569,LEOPARD 2 - SPARE PARTS (GRK(W8486-162741/000/A)),LEOPARD 2 - PIECES DE RECHANGE (GRK(W8486-162741/000/A)),https://buyandsell.gc.ca/procurement-data/tender-notice/PW-15-00700569,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-15-00700569,N7690,QC,INT
```

**URL:** http://bas-api.megginson.com/contracts.csv?keywords=baking

**Result:**

```
contract,title_en,title_fr,date_awarded,date_expires,value,supplier,supplier_city,supplier_region,buyer_en,buyer_fr,gsins,url_en,url_fr
W8486-122288/001/PR,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2015-03-04,2015-12-16,0.00,MIL-QUIP GROUPE TULMAR INC,St-Jean-sur-Richelieu,Quebec,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W8486-122288-001-PR,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8486-122288-001-PR
W8486-151508/001/PR,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2014-09-22,2016-01-31,146370.00,CROSS COUNTRY PARTS DISTRIBUTORS LTD,Calgary,Alberta,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W8486-151508-001-PR,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8486-151508-001-PR
W8486-151118/004/PR,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2015-03-03,2016-02-24,1253.00,PROTOCAN,Greely,Ontario,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W8486-151118-004-PR,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8486-151118-004-PR
W8482-156567/001/PR,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2015-01-23,2016-03-31,145164.00,BIG ERICS INC,DARTMOUTH,Nova Scotia,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W8482-156567-001-PR,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8482-156567-001-PR
W8482-156615/001/PR,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2015-04-01,2016-04-01,25576.00,MAISON RONDEAU,Québec,Quebec,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W8482-156615-001-PR,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8482-156615-001-PR
W0105-15F011/001/MCT,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2015-07-24,2016-07-31,468950.00,CHANDLER SUPPLIERS TO BUSINESS AND INDUSTRY,Saint John,New Brunswick,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W0105-15F011-001-MCT,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W0105-15F011-001-MCT
W8482-134705/001/PR,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2013-09-12,2016-09-12,25543.00,MAISON RONDEAU,Québec,Quebec,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W8482-134705-001-PR,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8482-134705-001-PR
W0127-13P009/001/EDM,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2013-09-16,2016-09-30,459415.00,ACTION MEALS,Kingston,Ontario,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W0127-13P009-001-EDM,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W0127-13P009-001-EDM
W8482-168010/001/PR,"Food, Cooking, Baking and Serving Equipment","Équipement pour la cuisson, la cuisson au four et le service des",2015-10-09,2016-12-09,103863.00,BIG ERICS INC,DARTMOUTH,Nova Scotia,Department of National Defence,Ministère de la défense nationale,N7310,https://buyandsell.gc.ca/procurement-data/contract-history/W8482-168010-001-PR,https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8482-168010-001-PR
```


### JSON output

**URL:** http://bas-api.megginson.com/tenders.json?gsins=N76,V2&delivery=ON,QC,NCR,CAN

**Result:**

```
[
  {
    "title_en": "AIR CHARTER SERVICES (E60SQ-020001/B)",
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-ZL-102-25299",
    "gsins": [
      "V201A",
      "V201B"
    ],
    "tender": "PW-$$ZL-102-25299",
    "regions_opportunity": [],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-ZL-102-25299",
    "regions_delivery": [
      "NCR",
      "ON",
      "QC"
    ],
    "title_fr": "SERVICES D'AFFR\u00c8TEMENT A\u00c9RIEN (E60SQ-020001/B)"
  },
  {
    "title_en": "AIRCRAFT RENTAL with Pilot(s) (W2037-150072/D)",
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-KIN-650-6679",
    "gsins": [
      "V204IA"
    ],
    "tender": "PW-$KIN-650-6679",
    "regions_opportunity": [],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-KIN-650-6679",
    "regions_delivery": [
      "NCR",
      "ON",
      "QC"
    ],
    "title_fr": "la location d'a\u00e9ronefs avec pilote(s) (W2037-150072/D)"
  },
  {
    "title_en": "Canada Post: Transportation Opportunities (Canada Post / Postes Canada)",
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00360795",
    "gsins": [
      "V204B"
    ],
    "tender": "PW-13-00360795",
    "regions_opportunity": [
      "CAN"
    ],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00360795",
    "regions_delivery": [
      "CAN"
    ],
    "title_fr": "Postes Canada: Occasions de Transport du courrier (Canada Post / Postes Canada)"
  },
  {
    "title_en": "Printing Logbooks and Combined Forms for Fisheries and Oceans Canada (F5211-130006)",
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-13-00538668",
    "gsins": [
      "N7610AA",
      "N7610D"
    ],
    "tender": "PW-13-00538668",
    "regions_opportunity": [
      "CAN"
    ],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-13-00538668",
    "regions_delivery": [
      "CAN"
    ],
    "title_fr": "Impression des journaux de bord et des formulaires combin\u00e9s pour P\u00eaches et Oc\u00e9ans Canada (F5211-130006)"
  },
  {
    "title_en": "LEOPARD 2 - SPARE PARTS (GRK(W8486-162741/000/A))",
    "url_en": "https://buyandsell.gc.ca/procurement-data/tender-notice/PW-15-00700569",
    "gsins": [
      "N7690"
    ],
    "tender": "PW-15-00700569",
    "regions_opportunity": [
      "INT"
    ],
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/appels-d-offres/PW-15-00700569",
    "regions_delivery": [
      "QC"
    ],
    "title_fr": "LEOPARD 2 - PIECES DE RECHANGE (GRK(W8486-162741/000/A))"
  }
]
```

**URL:** http://bas-api.megginson.com/contracts.json?keywords=baking

**Result:**

```
[
  {
    "date_expires": "2015-12-16",
    "contract": "W8486-122288/001/PR",
    "buyer_fr": "Minist\u00e8re de la d\u00e9fense nationale",
    "value": "0.00",
    "buyer_en": "Department of National Defence",
    "gsins": [
      "N7310"
    ],
    "supplier": "Mil-Quip Groupe Tulmar Inc.",
    "supplier_region": "Quebec",
    "supplier_city": "St-Jean-sur-Richelieu",
    "url_en": "https://buyandsell.gc.ca/procurement-data/contract-history/W8486-122288-001-PR",
    "date_awarded": "2015-03-04",
    "title_fr": "\u00c9quipement pour la cuisson, la cuisson au four et le service des",
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8486-122288-001-PR",
    "title_en": "Food, Cooking, Baking and Serving Equipment"
  },
  {
    "date_expires": "2016-01-31",
    "contract": "W8486-151508/001/PR",
    "buyer_fr": "Minist\u00e8re de la d\u00e9fense nationale",
    "value": "146370.00",
    "buyer_en": "Department of National Defence",
    "gsins": [
      "N7310"
    ],
    "supplier": "CROSS COUNTRY PARTS DISTRIBUTORS LTD",
    "supplier_region": "Alberta",
    "supplier_city": "Calgary",
    "url_en": "https://buyandsell.gc.ca/procurement-data/contract-history/W8486-151508-001-PR",
    "date_awarded": "2014-09-22",
    "title_fr": "\u00c9quipement pour la cuisson, la cuisson au four et le service des",
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8486-151508-001-PR",
    "title_en": "Food, Cooking, Baking and Serving Equipment"
  },
  {
    "date_expires": "2016-02-24",
    "contract": "W8486-151118/004/PR",
    "buyer_fr": "Minist\u00e8re de la d\u00e9fense nationale",
    "value": "1253.00",
    "buyer_en": "Department of National Defence",
    "gsins": [
      "N7310"
    ],
    "supplier": "Protocan",
    "supplier_region": "Ontario",
    "supplier_city": "Greely",
    "url_en": "https://buyandsell.gc.ca/procurement-data/contract-history/W8486-151118-004-PR",
    "date_awarded": "2015-03-03",
    "title_fr": "\u00c9quipement pour la cuisson, la cuisson au four et le service des",
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8486-151118-004-PR",
    "title_en": "Food, Cooking, Baking and Serving Equipment"
  },
  {
    "date_expires": "2016-03-31",
    "contract": "W8482-156567/001/PR",
    "buyer_fr": "Minist\u00e8re de la d\u00e9fense nationale",
    "value": "145164.00",
    "buyer_en": "Department of National Defence",
    "gsins": [
      "N7310"
    ],
    "supplier": "BIG ERICS INC",
    "supplier_region": "Nova Scotia",
    "supplier_city": "DARTMOUTH",
    "url_en": "https://buyandsell.gc.ca/procurement-data/contract-history/W8482-156567-001-PR",
    "date_awarded": "2015-01-23",
    "title_fr": "\u00c9quipement pour la cuisson, la cuisson au four et le service des",
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8482-156567-001-PR",
    "title_en": "Food, Cooking, Baking and Serving Equipment"
  },
  {
    "date_expires": "2016-04-01",
    "contract": "W8482-156615/001/PR",
    "buyer_fr": "Minist\u00e8re de la d\u00e9fense nationale",
    "value": "25576.00",
    "buyer_en": "Department of National Defence",
    "gsins": [
      "N7310"
    ],
    "supplier": "Maison Rondeau",
    "supplier_region": "Quebec",
    "supplier_city": "Qu\u00e9bec",
    "url_en": "https://buyandsell.gc.ca/procurement-data/contract-history/W8482-156615-001-PR",
    "date_awarded": "2015-04-01",
    "title_fr": "\u00c9quipement pour la cuisson, la cuisson au four et le service des",
    "url_fr": "https://achatsetventes.gc.ca/donnees-sur-l-approvisionnement/contrats-octroyes/W8482-156615-001-PR",
    "title_en": "Food, Cooking, Baking and Serving Equipment"
  }
]
```


## Coming soon ...

* Fuzzy lookup support: if there are no exact GSIN matches, look for something sort-of similar. [#6](https://github.com/PWGSC-DEEN/procurement-data-api/issues/6)
* Docker setup script (to build as a container).  [#7](https://github.com/PWGSC-DEEN/procurement-data-api/issues/7)

