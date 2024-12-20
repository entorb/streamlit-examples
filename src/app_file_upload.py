"""File Upload."""

import re
from io import StringIO

import chardet  # pip install chardet
import streamlit as st

# set max file size in config.toml
uploaded_file = st.file_uploader("Upload file", type="txt")

if uploaded_file:
    raw_data = uploaded_file.getvalue()
    # guess encoding
    result = chardet.detect(raw_data)
    if result["encoding"] and result["confidence"] > 0.5:  # noqa: PLR2004
        encoding = result["encoding"]
    else:
        encoding = "utf-8"  # UTF-8 as default
    s = StringIO(raw_data.decode(encoding)).read()
    assert s is not None  # noqa: S101

    s = s.replace("\r", "")
    # remove last linebreaks
    s = re.sub(r"[\n\s]+$", "", s)
    st.write(s.split("\n"))
