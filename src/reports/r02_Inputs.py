"""Selects and Filters."""  # noqa: N999

import pandas as pd
import streamlit as st

from helper import get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore


def reset_filters() -> None:  # noqa: D103
    st.session_state.sel_year = None


st.header("Simple Inputs")
st.subheader("Slider")
POP = st.session_state.get("sel_pop", 2000)
sel_pop = st.slider("Select Population", 100, 5000, 2000, 25, key="sel_pop")


st.header("Select with reset button")

data = {"year": [2020, 2021, 2022, 2020, 2021, 2022], "value": [1, 2, 3, 3, 2, 1]}
df = pd.DataFrame(data)

cols = st.columns((1, 1, 4))

sel_year = cols[0].selectbox(
    label="Year",
    options=range(df["year"].min(), df["year"].max() + 1),
    index=None,
    key="sel_year",
)
if sel_year:
    df = df.query("year == @sel_year")

cols[1].button("Reset", on_click=reset_filters)
cols[2].write(df)


st.header("Multi-Select")
cols = st.columns((1, 1, 4))
sel_years = cols[0].multiselect(
    label="Year",
    options=range(df["year"].min(), df["year"].max() + 1),
)
if sel_years:
    df = df.query("year in @sel_years")
    cols[2].write(df)


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

cols = st.columns((1, 5))
sel = cols[0].selectbox(
    label="Select Department",
    options=lst,
    index=idx,
)

# after selection: update url parameter and session state
if sel:
    st.query_params[key] = sel
    st.session_state[key] = sel
