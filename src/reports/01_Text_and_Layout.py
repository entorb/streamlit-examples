"""Sections_and_Text."""

import streamlit as st

from helper import get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore

st.header("Columns")
st.subheader("3 same size columns")

col1, col2, col3 = st.columns(3)
col1.subheader("Col1")
col2.subheader("Col2")
col3.subheader("Col3")

st.subheader("1/3 and 3/4 columns with only the first used")
col1, _ = st.columns([1, 3])  # 1/3 and 3/4 columns
col1.subheader("Col1")
