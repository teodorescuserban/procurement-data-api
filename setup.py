#!/usr/bin/python

from setuptools import setup
import sys

if sys.version_info[0] < 3:
    sys.exit("ERROR: requires Python 3 or higher.")

setup(
    name = 'bas-api',
    packages = ['bas'],
    version = '0.1',
    description = 'Flask-based API for procurement data from BuyAndSell.gc.ca',
    author='David Megginson',
    author_email='contact@megginson.com',
    url='https://github.com/PWGSC-DEEN/procurement-data-api',
    install_requires=['flask', 'pymysql'],
    test_suite='tests'
)
