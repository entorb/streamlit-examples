"""File Upload."""

import re
from io import StringIO

import chardet  # pip install chardet
import streamlit as st

from helper import filename_to_title, get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(filename_to_title(__file__))


def guess_encoding(raw_data: bytes) -> str:  # noqa: D103
    result = chardet.detect(raw_data)
    if result["encoding"] and result["confidence"] > 0.5:  # noqa: PLR2004
        return result["encoding"]
    return "utf-8"  # as fallback


st.header("Upload a text file (and guess encoding)")

st.write("set `maxUploadSize` in config.toml")

uploaded_file = st.file_uploader("Upload file", type="txt")

if uploaded_file:
    raw_data = uploaded_file.getvalue()
    encoding = guess_encoding(raw_data)
    s = StringIO(raw_data.decode(encoding)).read()
    # some cleanup
    s = s.replace("\r", "")
    s = re.sub(r"[\n\s]+$", "", s)
    st.write(s.split("\n"))
