# Simple API for procurement data

_Started by David Megginson, 2015-10_

## Setup

**Note:** requires Python3.  This will not work with Python 2.7.

1. Create a new MySQL database (e.g. "bas").
2. Set up the database schema: ``mysql bas < sql/schema.sql``
3. Set up a Python virtualenv for the app: ``mkvirtualenv -p /usr/bin/python3 bas``
4. Install flask: ``pip install flask``

## Running (single thread)

```
python api.py
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
      "GLB"
    ],
    "regions_delivery": [
      "QC"
    ],
    "tender": "PW-15-00700569"
  }
]
```

## Coming soon ...

* ``setup.py`` file (to automatically download and install dependencies)
* WSGI script (for running in a multi-threaded browser)
* Docker setup script (to build as a container)
* Support for contract history and GSIN lookup (handles only tender notices right now)
* Fuzzy lookup support: if there are no exact GSIN matches, look for something sort-of similar.
* Output formats beyond JSON (CSV and XML).

