#!/bin/sh

# ensure we are in the root dir
cd $(dirname $0)/..

# exit upon error
set -e

uv remove chardet msal pandas streamlit xlsxwriter
uv remove --dev ruff pytest pytest-cov tomli-w watchdog

uv lock --upgrade
uv sync --upgrade

uv add chardet msal pandas streamlit xlsxwriter
uv add --dev ruff pytest pytest-cov tomli-w watchdog

uv lock --upgrade
uv sync --upgrade

# ruff
uv run ruff format
uv run ruff check --fix

# pre-commit
prek autoupdate
prek run --all-files

echo DONE
