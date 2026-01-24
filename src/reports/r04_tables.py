"""Tables."""

import datetime as dt

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

st.header("Simple Tables")
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
    width="content",
)

st.header("From raw data to Top 10")


def gen_random_data(rows: int = 100) -> pd.DataFrame:
    """Generate random data."""
    rng = np.random.default_rng()
    dt_offset = dt.datetime(2025, 1, 1, 0, 0, 0, tzinfo=None)  # noqa: DTZ001
    names = ["cat 1", "cat 2", "cat 3"]
    data = [
        {
            "datetime": dt_offset
            + dt.timedelta(seconds=int(rng.integers(0, 86400) * 31)),
            "category": rng.choice(names),
            "value": int(rng.integers(0, 100)),
        }
        for _ in range(rows)
    ]
    df = pd.DataFrame(data).sort_values("datetime").reset_index(drop=True)
    return df


def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich the dataframe by extracting data of datetime column."""
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["day"] = df["datetime"].dt.day
    df["hour"] = df["datetime"].dt.hour
    df["value_rounded"] = df["value"].round(-1)
    return df


df = gen_random_data()
st.subheader("Raw data")
st.dataframe(df, hide_index=True)

df = enrich_data(df)

st.subheader("Top10")
rel_cols = st.multiselect(
    label="column",
    options=["category", "day", "hour", "value_rounded"],
    default=["category", "hour", "value_rounded"],
)

if rel_cols:
    cols = st.columns(len(rel_cols))
    for i, col in enumerate(rel_cols):
        cols[i].write(col.title().replace("_", " "))
        df2 = df.groupby(col).size().to_frame("count")
        cols[i].dataframe(
            df2.head(10).sort_values(["count", col], ascending=[False, True])
        )
