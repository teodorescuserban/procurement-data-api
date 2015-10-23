# Simple API for procurement data

_Started by David Megginson, 2015-10_

## Setup

**Note:** requires Python3.  This will not work with Python 2.7.

1. Create a new MySQL database (e.g. "bas").
2. Set up the database schema: ``mysql bas < sql/schema.sql``
3. Copy the ``config.py.TEMPLATE`` file to ``config.py`` and fill in your local database connection information.
4. Set up a Python virtualenv for the app: ``mkvirtualenv -p /usr/bin/python3 bas``
5. Install flask: ``pip install flask``
6. Download [procurement data](https://buyandsell.gc.ca/procurement-data/csv/tender/active) from BuyAndSell.
7. Load the data into the database: ``python load_data.py tpsgc-pwgsc_ao-t_a.csv``

## Running (single thread)

```
python bas/api.py
```

## Usage

The path ``tender-notices.json`` returns a list of tender notices in a JSON-based encoding. By default, it returns all active tender notices, but you can filter results using the following GET parameters (all optional):

``gsins`` — a comma-separated list of GSIN-code prefixes to match, e.g. ``gsins=N7610,V204``.  These will match any GSIN codes that begin with those letters, e.g. _N7610AA_ or _V204B._  A tender notice needs to match only one of the GSIN codes.

``delivery`` — a comma-separated list of codes to match for the region of delivery, e.g. ``delivery=ON,QC,NCR``.  In addition to the two-letter codes for the 13 provinces and territories, some tender notices may include ``NCR`` for the national-capital region, ``CAN`` for Canada-wide, ``ABL`` for aboriginal lands, ``USA`` for the United States, ``MEX`` for Mexico, or ``INT`` for international.  Tender notices are not consistent, and may (for example) list ``CAN``, all of the province codes separately, or both to indicate a tender that applies to the whole country.

``opportunity`` — a comma-separated list of codes to match for the region of opportunity, e.g. ``opportunity=PE,NS,NB``.  The codes are the same as for the _delivery_ parameter.

## Example

Find all tender notices that have a GSIN code starting with "N76" or "V2", and a delivery region of Ontario, Quebec, the National Capital Region, or Canada-wide:

```
http://example.org/tender-notices.json?gsins=N76,V2&delivery=ON,QC,NCR,CAN
```

Result:

```
[
  {
    "title_en": "Canada Post: Transportation Opportunities (Canada Post / Postes Canada)",
    "title_fr": "Postes Canada: Occasions de Transport du courrier (Canada Post / Postes Canada)",
    "gsins": [
      "V204B"
    ],
    "regions_opportunity": [
      "CAN"
    ],
    "regions_delivery": [
      "CAN"
    ],
    "tender": "PW-13-00360795"
  },
  {
    "title_en": "Printing Logbooks and Combined Forms for Fisheries and Oceans Canada (F5211-130006)",
    "title_fr": "Impression des journaux de bord et des formulaires combin\u00e9s pour P\u00eaches et Oc\u00e9ans Canada (F5211-130006)",
    "gsins": [
      "N7610AA",
      "N7610D"
    ],
    "regions_opportunity": [
      "CAN"
    ],
    "regions_delivery": [
      "CAN"
    ],
    "tender": "PW-13-00538668"
  },
  {
    "title_en": "LEOPARD 2 - SPARE PARTS (GRK(W8486-162741/000/A))",
    "title_fr": "LEOPARD 2 - PIECES DE RECHANGE (GRK(W8486-162741/000/A))",
    "gsins": [
      "N7690"
    ],
    "regions_opportunity": [
      "INT"
    ],
    "regions_delivery": [
      "QC"
    ],
    "tender": "PW-15-00700569"
  }
]
```

## Coming soon ...

* WSGI script (for running in a multi-threaded browser) [#1](https://github.com/PWGSC-DEEN/procurement-data-api/issues/1)
* ``setup.py`` file (to automatically download and install dependencies) [#2](https://github.com/PWGSC-DEEN/procurement-data-api/issues/2)
* Support for contract history and GSIN lookup (handles only tender notices right now) [#3](https://github.com/PWGSC-DEEN/procurement-data-api/issues/3) and  [#4](https://github.com/PWGSC-DEEN/procurement-data-api/issues/4)
* Output formats beyond JSON (CSV and XML).  [#5](https://github.com/PWGSC-DEEN/procurement-data-api/issues/5)
* Fuzzy lookup support: if there are no exact GSIN matches, look for something sort-of similar. [#6](https://github.com/PWGSC-DEEN/procurement-data-api/issues/6)
* Docker setup script (to build as a container).  [#7](https://github.com/PWGSC-DEEN/procurement-data-api/issues/7)

