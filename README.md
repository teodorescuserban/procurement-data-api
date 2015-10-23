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

## Coming soon ...

* ``setup.py`` file (to automatically download and install dependencies)
* WSGI script (for running in a multi-threaded browser)
* Docker setup script (to build as a container)
* Support for contract history and GSIN lookup (handles only tender notices right now)
* Fuzzy lookup support: if there are no exact GSIN matches, look for something sort-of similar.
* Output formats beyond JSON (CSV and XML).

