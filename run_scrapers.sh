#!/bin/bash

echo "Running scrapers for government COVID-19 measures for the states of New England"

python3 Scrapers/ct.py
python3 Scrapers/ma.py
python3 Scrapers/vt.py
python3 Scrapers/ri.py
python3 Scrapers/nh.py
python3 Scrapers/me.py
