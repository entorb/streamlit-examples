"""Charts."""

# ruff: noqa: NPY002

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from helper import get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore

st.header("x-y Line Charts")

df = pd.DataFrame({"x": range(100)})
# y = sin(x) + noise
noise = np.random.rand(len(df)) * 0.1
df["y"] = np.sin(df["x"] / 25 * np.pi) + noise

st.subheader("quick and simple: st.line_chart")
st.line_chart(df, x="x", y="y", x_label="", y_label="")

st.subheader("same via alt.Chart")
c = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("x", title=None),
        y=alt.Y("y", title=None),
    )
)
st.altair_chart(c, use_container_width=True)


st.subheader("Lines and Points, with mean and linear regression")
base = (
    alt.Chart(df, title="Chart Title")
    .mark_point(size=100)
    .encode(
        x=alt.X("x", title=None),
        y=alt.Y("y", title=None),
    )
)
mean_line = (
    alt.Chart(df)
    .mark_rule(color="gray", strokeDash=[6, 2], strokeWidth=1)  # rule not line!
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

st.subheader("quick and simple: st.bar_chart for above data")
st.bar_chart(df, x="x", y="y", x_label="", y_label="")

st.subheader("st.bar_chart with multiple columns")
df = pd.DataFrame(np.random.rand(20, 3), columns=["a", "b", "c"])
st.bar_chart(df, stack=True, horizontal=False)

st.subheader("more advanced and flexible: alt.Chart for time series")

# generate date series and convert to strings of "yyyy-mm"
# date strings are nice for multi language apps
df = pd.DataFrame(
    {
        "month": pd.date_range(start="2023-01", end="2024-12", freq="MS").strftime(
            "%Y-%m"
        )
    }
)
# add column group with 2 values per month
df = pd.concat(
    [
        df.assign(group="group1"),
        df.assign(group="group2"),
    ]
).sort_values("month")
# add random value column
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
