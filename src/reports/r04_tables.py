"""Tables."""

import numpy as np
import pandas as pd
import streamlit as st

from helper import filename_to_title, get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(filename_to_title(__file__))


df = pd.DataFrame(
    data={
        "id": range(123456, 123466),
        "name": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        "value": np.random.default_rng().random(10),
        "date": pd.date_range("2025-01-01", periods=10),
    }
)

st.header("simple tables")
st.subheader("st.write")
st.write(df)

# st.subheader("st.table")
# st.table(df)

st.subheader("st.dataframe")
st.dataframe(df)

st.subheader("st.dataframe with column_config and reduced columns")
df["url"] = "https://www.somewhere.com/path/" + df["id"].astype(str)
st.dataframe(
    df,
    hide_index=True,
    column_config={
        "date": st.column_config.DateColumn(format="YYMMDD"),
        "url": st.column_config.LinkColumn("ID", display_text=r"/(\d+)$"),
        "value": st.column_config.ProgressColumn(
            format="%.2f", min_value=0, max_value=1
        ),
    },
    column_order=["url", "date", "value"],
    use_container_width=False,
)
