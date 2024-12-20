"""Simple Minimal App."""

from pathlib import Path

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

col1, col2 = st.columns([1, 9])  # 1/10 and 9/10 columns
col1.subheader("MySubHeader")

logger.info("End")
