#!/bin/sh

# ensure we are in the root dir
cd $(dirname $0)/..

# exit upon error
set -e

uv remove chardet msal pandas streamlit xlsxwriter
uv remove --dev ruff pre-commit pytest pytest-cov tomli-w watchdog

uv lock --upgrade
uv sync --upgrade

uv add chardet msal pandas streamlit xlsxwriter
uv add --dev ruff pre-commit pytest pytest-cov tomli-w watchdog

uv lock --upgrade
uv sync --upgrade

echo DONE
