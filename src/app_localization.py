"""Localization."""

import json
from pathlib import Path

# ruff: noqa: E501
import altair as alt
import pandas as pd
import streamlit as st

# Download d3-format and d3-time-format locale files
# wget https://raw.githubusercontent.com/d3/d3-format/master/locale/de-DE.json -out src/resources/d3-format-de-DE.json
# wget https://raw.githubusercontent.com/d3/d3-time-format/master/locale/de-DE.json -out src/resources/d3-time-format-de-DE.json
# wget https://raw.githubusercontent.com/d3/d3-format/master/locale/en-US.json -out src/resources/d3-format-en-US.json
# wget https://raw.githubusercontent.com/d3/d3-time-format/master/locale/en-US.json -out src/resources/d3-time-format-en-US.json
# alternatively: hard code as dict


# Chart localization
@st.cache_resource
def get_d3_locale(lang: str) -> tuple[dict, dict]:
    """
    Get d3-format and d3-time-format locale files for given language.

    Used for localization of altair charts.
    """
    locale = "de-DE" if lang == "de" else "en-US"
    with Path(f"src/resources/d3-format-{locale}.json").open() as f:
        d3_format = json.load(f)
    with Path(f"src/resources/d3-time-format-{locale}.json").open() as f:
        d3_time_format = json.load(f)
    return d3_format, d3_time_format


# translation dictionaries
dictionary = {
    "en": {
        # "locale": "en_US",
        "format:date": "YYYY-MM-DD",
        "col:date": "Date",
        "col:status": "Status",
        "col:cnt": "Count",
        "value:open": "open",
        "value:closed": "closed",
    },
    "de": {
        # "locale": "de_DE",
        "format_date": "DD.MM.YYYY",
        "col:date": "Datum",
        "col:status": "Status",
        "col:cnt": "Anzahl",
        "value:open": "Offen",
        "value:closed": "Geschlossen",
    },
}

# Dummy data
df = pd.DataFrame(
    {
        "date": pd.date_range(start="2021-01-01", periods=12, freq="MS"),
        "status": ["open", "closed"] * 6,
        "cnt": [1000, 2000] * 6,
    }
)
# set some NN values
df.loc[1, "cnt"] = None
df.loc[3, "cnt"] = pd.NA


# select language
st.session_state["USER_LANG"] = st.selectbox("Select language", ["en", "de"])
lang = st.session_state["USER_LANG"]  # shortcut


def tl(key: str) -> str:
    """Shortcut for translation."""
    return dictionary[lang][key]


def translate_df_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Translate DataFrame Columns."""
    d = {}
    lst = [x[4:] for x in dictionary[lang] if x.startswith("col:")]

    for col in df.columns:
        if col in lst:
            d[col] = tl("col:" + col)
    if d:
        df = df.rename(columns=d)
    return df


d3_format, d3_time_format = get_d3_locale(lang)

# The following locale setting code is not in use
#  because Streamlit does not support locale settings for charts directly.
# import locale
# locale.setlocale(locale.LC_ALL, d[lang]["locale"])  # de_DE, en_US


# dataframe: translate status values
df["status"] = df["status"].map(
    {"open": tl("value:open"), "closed": tl("value:closed")}
)

# dataframe column names: 2 ways
# 1. keep original column names and use translation in chart and table
# table: st.dataframe(column_config("cnt": tl("cnt"))
# chart: y=alt.Y("cnt:Q", title=tl("cnt"))
# 2. rename columns in dataframe
# I prefer 2, because of less redundancy

df = translate_df_columns(df)
col_date = tl("col:date")
col_status = tl("col:status")
col_cnt = tl("col:cnt")

# display dataframe as table
# using df.style.format for localization
# and st.column_config for date formatting
st.dataframe(
    # df,
    # see https://datascientyst.com/style-pandas-dataframe-like-pro-examples/
    df.style.format(
        decimal=d3_format["decimal"],
        thousands=d3_format["thousands"],
        precision=0,  # default is 5 digits
        # na_rep="",  # not working
    ),
    # https://docs.streamlit.io/develop/api-reference/data/st.column_config
    column_config={
        col_date: st.column_config.DateColumn(format=tl("format:date")),
        # col_cnt: st.column_config.NumberColumn(format=d3_format["decimal"]),
    },
    hide_index=True,
    width=800,
)


# Chart
chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X(f"yearmonth({col_date}):T", title=col_date),
        y=alt.Y(f"{col_cnt}:Q"),
        color=alt.Color(f"{col_status}:N"),
        tooltip=[
            alt.Tooltip(f"yearmonth({col_date}):T", title=col_date),
            alt.Tooltip(f"{col_status}:N"),
            alt.Tooltip(f"{col_cnt}:Q"),
        ],
    )
)

# Chart localization
# not working in Streamlit:
# alt.renderers.set_embed_options(format_locale="de-DE", time_format_locale="de-DE")
# from https://altair-viz.github.io/user_guide/customization.html#localization

# alternative solution: set via usermeta
# inspired from https://github.com/streamlit/streamlit/issues/1161,
#  removed depencancy to vl_convert
chart = chart.properties(
    usermeta={
        "embedOptions": {
            "formatLocale": d3_format,
            "timeFormatLocale": d3_time_format,
        }
    }
)
st.altair_chart(chart, width="stretch")
