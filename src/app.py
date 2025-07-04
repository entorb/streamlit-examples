"""
Main file.

Creates navigation for file in reports dir.
"""

import tracemalloc
from time import time

import streamlit as st

from helper import create_navigation_menu, get_logger_from_filename

MEASURE_MEMORY = True
logger = get_logger_from_filename(__file__)


def main() -> None:  # noqa: D103
    # must be first Streamlit command
    st.set_page_config(
        page_title="Torben's Streamlit Examples", page_icon=None, layout="wide"
    )

    if MEASURE_MEMORY:
        tracemalloc.start()
    time_start = time()
    pagename = create_navigation_menu()
    time_end = time()
    log_line = f"stats: {pagename},{round(time_end - time_start, 1)}s"

    if MEASURE_MEMORY:
        max_bytes = tracemalloc.get_traced_memory()[0]
        tracemalloc.stop()
        log_line += f",{round(max_bytes / 1_048_576, 1)}MB"
    logger.info(log_line)


if __name__ == "__main__":
    try:
        main()
    # custom exception handling is required for Sentry.
    except Exception as e:
        logger.exception("Exception:")
        st.exception(e)
        st.stop()
