#!/bin/sh
cd $(dirname $0)/..

streamlit run src/app.py
# for production better use
# python -OO -m streamlit run src/app.py
