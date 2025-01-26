"""Sections and Text."""

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


# st.header("Dark Layout Toggle")
# toggle_dark = st.toggle("Dark Layout", value=True)
# if st.get_option("theme.base") == "light" and toggle_dark:
#     st._config.set_option("theme.base", "dark")  # type: ignore
#     st.rerun()
# elif st.get_option("theme.base") == "dark" and not toggle_dark:
#     st._config.set_option("theme.base", "light")  # type: ignore
#     st.rerun()
