"""Simple Minimal App."""

from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

logger = get_logger(Path(__file__).stem)  # filename as logger name
logger.info("Start")

st.set_page_config(page_title="AppTitle", page_icon=None, layout="wide")
st.title("MyPageTitle")
st.header("MyHeader")
st.subheader("MySubHeader")
sel_param = st.selectbox("Parameter", ("count", "sum"))

col1, col2, col3 = st.columns(3)  # 3 same size columns
col1.subheader("MySubHeader")

col1, _ = st.columns([1, 3])  # 1/3 and 3/4 columns
col1.subheader("MySubHeader")


st.header("Filtering")


def reset_filters() -> None:
    st.session_state.sel_year = None


# example data
data = [(2020, 123), (2021, 124)]
df = pd.DataFrame(data, columns=["year", "value"])
col1, col2, col3, col4, col5, col6 = st.columns(6)

sel_year = col1.selectbox(
    "Year",
    options=range(df["year"].min(), df["year"].max() + 1),
    index=None,
    key="sel_year",
)
if sel_year:
    df = df.query("year == @sel_year")
col2.button("Reset", on_click=reset_filters)
st.write(df)


logger.info("End")
