#!/bin/bash

echo "Running scrapers for government COVID-19 measures for the states of New England"
python3 ct.py
python3 ma.py
python3 vt.py
python3 ri.py
python3 nh.py
python3 me.py
