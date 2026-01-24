# Streamlit Examples / Snippets

Some code examples using Python [Streamlit](https://streamlit.io).

## Contents

* [app.py](src/app.py): Main app including multiple examples in [src/reports](src/reports/)
  * [Selects](src/reports/r02_Selects.py): selects, filter, read write url parameters
  * [Charts](src/reports/r03_Charts.py): x-y-lines, regression, mean; bar charts
  * [Tables](src/reports/r04_Tables.py): simple to fancy tables
  * [Data_Editor](src/reports/r05_Data_Editor.py): data editor with save button
  * [File_Download](src/reports/r11_File_Download.py): Download data as text or Excel file
  * [File_Upload](src/reports/r12_File_Upload.py): Upload data
* Stand-alone example apps
  * [app_azure_login_msal.py](src/app_azure_login_msal.py): Azure Login/Authentication using MSAL
  * [app_db_con_limit.py](src/app_db_con_limit.py): Database access, using connection pool to restrict concurrent connections
  * [app_localization.py](src/app_localization.py): Language localization

## Repo Setup

### Install

Requires [UV](https://docs.astral.sh/uv/) package manager

### Update dependencies

see [update.sh](scripts/update.sh)

### Run

see [run.sh](scripts/run.sh)

### Check Code

```sh
uv run ruff format
uv run ruff check
uv run pre-commit run --all-files
uv run pytest --cov --cov-report=html:coverage_report
```

are executed via a [GitHub Action](.github/workflows/check.yml)

### Config

see [.streamlit/config.toml](.streamlit/config.toml)
can be converted to `config-prod.toml` via [scripts/config_convert.py](scripts/config_convert.py)

## Links

### My Streamlit Projects

* <https://github.com/entorb/strava-streamlit>
* <https://github.com/entorb/de-dorf>

### Other Python Examples/Snippets

* <https://github.com/entorb/template-python>
* <https://entorb.net/wickie/Python>
* <https://entorb.net/wickie/Pandas>

## SonarQube Code Analysis

At [sonarcloud.io](https://sonarcloud.io/summary/overall?id=entorb_streamlit-examples&branch=main)
