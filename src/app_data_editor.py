"""Data Editor with Save Button."""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

logger = get_logger(Path(__file__).stem)  # filename as logger name
logger.info("Start")


st.set_page_config(page_title="AppTitle", page_icon=None, layout="wide")

data = (("No1", 12, 13), ("No2", 14, 15))
df = pd.DataFrame(data, columns=["Name", "Lat", "Lng"])

df_edited = st.data_editor(df, hide_index=True, num_rows="dynamic")
if st.button("Save"):
    df2 = df_edited[["Lat", "Lng", "Name"]]
    df2[["Lat", "Lng"]] = df2[["Lat", "Lng"]].replace(0, np.nan)
    df2["Name"] = df2["Name"].str.strip().replace("", np.nan)
    df2 = df2.dropna()
    # trim and round
    df2["Lat"] = df2["Lat"].clip(lower=-180, upper=180).round(4)
    df2["Lng"] = df2["Lng"].clip(lower=-90, upper=90).round(4)
    df2 = df2.sort_values("Name")
    p = Path("filename.txt")
    df2.to_csv(p, sep="\t", index=False, header=True, lineterminator="\n")
    st.rerun()

logger.info("End")
