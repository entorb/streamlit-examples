"""
Main file for files in reports dir.

Should handle general setup and navigation.
"""

import streamlit as st

from helper import create_navigation_menu, get_logger_from_filename

MEASURE_MEMORY = True

# must be first Streamlit command
st.set_page_config(page_title="AppTitle", page_icon=None, layout="wide")
logger = get_logger_from_filename(__file__)
logger.info("Start")

# start measurement of memory usage and runtime
if MEASURE_MEMORY:
    import tracemalloc
    from time import time

    tracemalloc.start()
    time_start = time()

pagename = create_navigation_menu()

# print memory usage and runtime
if MEASURE_MEMORY:
    time_end = time()
    max_bytes = tracemalloc.get_traced_memory()[0]
    print(f"{round(max_bytes / 1_048_576, 1)}MB, {round(time_end - time_start, 1)}s")

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

    tracemalloc.stop()

logger.info(f"End: {pagename}")
