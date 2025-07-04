"""Data Editor with Save Button."""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from helper import filename_to_title, get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(filename_to_title(__file__))


# generate list of A-J
names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
lats = [40 + 1.234 / i for i in range(1, 11)]
lons = [11 + 1.234 / i for i in range(1, 11)]
df = pd.DataFrame(data={"Name": names, "Lat": lats, "Lng": lons})

df_edited = st.data_editor(df, hide_index=True, num_rows="dynamic")
if st.button("Save"):
    # change column order
    df2 = df_edited[["Lat", "Lng", "Name"]]
    # clean up
    df2[["Lat", "Lng"]] = df2[["Lat", "Lng"]].replace(0, np.nan)
    df2["Name"] = df2["Name"].str.strip().replace("", np.nan)
    df2 = df2.dropna()
    # trim and round
    df2["Lat"] = df2["Lat"].clip(lower=-180, upper=180).round(4)
    df2["Lng"] = df2["Lng"].clip(lower=-90, upper=90).round(4)
    df2 = df2.sort_values("Name")
    p = Path("out/filename.csv")
    df2.to_csv(p, sep="\t", index=False, header=True, lineterminator="\n")
    st.write(f"written to `{p}`")
