#!/usr/bin/env python3

"""Run a local dev copy of the API without logging to STDERR"""
import sys
from bas.api import app
app.run(debug=True, host='0.0.0.0')
