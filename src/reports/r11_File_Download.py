"""File Download."""  # noqa: N999

import io

import numpy as np
import pandas as pd
import streamlit as st

from helper import get_logger_from_filename

# pip install xlsxwriter

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore


st.header("Download a text file")
st.write("Prepare step makes sense if calculations are needed.")
col1, col2, _ = st.columns((1, 1, 6))
if col1.button(label="File Prepare"):
    cont = """This is the content of the text file."""
    buffer = io.BytesIO()
    buffer.write(cont.encode("utf-8"))
    buffer.seek(0)

    col2.download_button(
        label="File Download",
        data=buffer,
        file_name="text.txt",
        mime="text/plain",
    )

st.header("Download DataFrame as Excel file")

st.write("this requires `pip install xlsxwriter`")
df = pd.DataFrame(
    data={
        "id": range(123456, 123466),
        "name": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        "value": np.random.default_rng().random(10),
        "date": pd.date_range("2025-01-01", periods=10),
    }
)
col1, col2, _ = st.columns((1, 1, 6))
if col1.button(label="Excel Prepare"):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        writer.close()

    col2.download_button(
        label="Excel Download",
        data=buffer,
        file_name="file.xlsx",
        mime="application/vnd.ms-excel",
    )
