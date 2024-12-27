"""Selects and Filters."""

import pandas as pd
import streamlit as st

from helper import get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore


st.header("Select with reset button")


def reset_filters() -> None:  # noqa: D103
    st.session_state.sel_year = None


data = {"year": [2020, 2021, 2022, 2020, 2021, 2022], "value": [1, 2, 3, 3, 2, 1]}
df = pd.DataFrame(data)

col1, col2, _ = st.columns((1, 1, 4))

sel_year = col1.selectbox(
    label="Year",
    options=range(df["year"].min(), df["year"].max() + 1),
    index=None,
    key="sel_year",
)
if sel_year:
    df = df.query("year == @sel_year")

col2.button("Reset", on_click=reset_filters)
st.write(df)


st.header("Multi-Select")
sel_years = st.multiselect(
    label="Year",
    options=range(df["year"].min(), df["year"].max() + 1),
)
if sel_years:
    df = df.query("type in @sel_years")


st.header("Select that reads and writes URL parameters")
lst = ["Dpt1", "Dpt2", "Dpt3"]
key = "sel_dpt"
# read url parameter and store as session state
if key in st.query_params:
    st.session_state[key] = st.query_params[key]
if key not in st.session_state:
    idx = 0
else:
    idx = lst.index(st.session_state[key]) if st.session_state[key] in lst else None

col1, _ = st.columns((1, 5))
sel = col1.selectbox(
    label="Select Department",
    options=lst,
    index=idx,
)

# after selection: update url parameter and session state
if sel:
    st.query_params[key] = sel
    st.session_state[key] = sel
