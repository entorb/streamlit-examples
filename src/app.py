"""
Main file for files in reports dir.

Should handle general setup and navigation.
"""

import streamlit as st

from helper import create_navigation_menu, get_logger_from_filename

# must be first Streamlit command
st.set_page_config(page_title="AppTitle", page_icon=None, layout="wide")
logger = get_logger_from_filename(__file__)
logger.info("Start")

create_navigation_menu()

logger.info("End")
