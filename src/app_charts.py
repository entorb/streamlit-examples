"""Chart Examples."""

# ruff: noqa: NPY002

from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

logger = get_logger(Path(__file__).stem)  # filename as logger name
logger.info("Start")

st.set_page_config(page_title="AppTitle", page_icon=None, layout="wide")

st.header("Simple x-y Line Chart")

# dataframe x: range 0 to 100, y: random, set x as index
# df = pd.DataFrame({"x": range(100), "y": np.random.rand(100)})
df = pd.DataFrame({"x": range(100)})
# y = sin(x) + noise
df["y"] = np.sin(df["x"] / 25 * np.pi) + np.random.rand(len(df)) * 0.1
# st.write(df)

# simple plot using st.line_chart
# st.subheader("st.line_chart")
# st.line_chart(df, x="x", y="y", x_label="", y_label="")

# st.subheader("using alt.Chart")

# c = (
#     alt.Chart(df)
#     .mark_line()
#     .encode(
#         x=alt.X("x", title=None),
#         y=alt.Y("y", title=None),
#     )
# )
# st.altair_chart(c, use_container_width=True)


st.subheader("Lines and Points using alt.Chart, with mean and linear regression")
base = (
    alt.Chart(df)
    .mark_point(size=100)
    .encode(
        x=alt.X("x", title=None),
        y=alt.Y("y", title=None),
    )
)
mean_line = (
    alt.Chart(df)
    .mark_rule(color="gray", strokeDash=[6, 2], strokeWidth=1)
    .encode(
        y="mean(y)",
    )
)
reg_line = base.transform_regression("x", "y").mark_line(
    color="gray", strokeDash=[4, 4], strokeWidth=1
)
c = base + base.mark_line() + mean_line + reg_line
st.altair_chart(c, use_container_width=True)  # type: ignore


st.header("Bar Charts")

# generate date series and convert to strings of "yyyy-mm"
df = pd.DataFrame(
    {
        "month": pd.date_range(start="2023-01", end="2024-12", freq="MS").strftime(
            "%Y-%m"
        )
    }
)
# add column group to each month
df = pd.concat(
    [
        df.assign(group="group1"),
        df.assign(group="group2"),
    ]
)
df["value"] = np.random.rand(df.shape[0])
# st.write(df)

# custom color scale
color_scale = alt.Scale(
    domain=["group1", "group2"],
    range=["#FF0000", "blue"],
)
c = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        # date axis, prints month names in English
        # x=alt.X("yearmonth(month):T", title=None),
        # simple print month numbers, preferred when in multi lang context
        x=alt.X("month:N", title=None),
        y=alt.Y("value:Q", title=None),
        # color="group:N",  # simple
        color=alt.Color("group:N", scale=color_scale),
        xOffset="group:N",  # remove to get stacked bars
        tooltip=["month:N", "group:N", "value:Q"],
    )
)
st.altair_chart(c, use_container_width=True)
# :T stands for Temporal. It indicates that the field contains date or time values.
# :N stands for Nominal. It indicates that the field contains categorical data,
#   which represents discrete categories or labels.
# :Q stands for Quantitative. It indicates that the field contains numerical data
#   that can be measured and compared.
logger.info("End")
