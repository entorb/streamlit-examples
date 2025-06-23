"""Charts."""

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from helper import filename_to_title, get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(filename_to_title(__file__))


st.header("x-y Line Charts")

df = pd.DataFrame({"x_col": range(100)})
RNG = np.random.default_rng(seed=42)
noise = RNG.random(len(df)) * 0.1
# y := sin(x) + noise
df["y_col"] = np.sin(df["x_col"] / 25 * np.pi) + noise

st.subheader("quick and simple: st.line_chart")
st.line_chart(df, x="x_col", y="y_col", x_label="", y_label="")

st.subheader("same via alt.Chart")
chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("x_col", title=None),
        y=alt.Y("y_col", title=None),
    )
)
st.altair_chart(chart, use_container_width=True)


st.subheader("x-y line line plot for data in wide table format")
df["y2_col"] = 0.8 * np.sin((df["x_col"] + 25) / 25 * np.pi) + noise
df = df.set_index("x_col")
st.write(df)
chart = (
    alt.Chart(df.reset_index())
    # wide table to long table
    .transform_fold(["y_col", "y2_col"], as_=["cols", "angle"])
    .mark_line()
    .encode(
        x=alt.X("x_col:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("angle:Q", title=None),
        color=alt.Color(
            "cols:N",
            scale=alt.Scale(
                domain=["y_col", "y2_col"],
                range=["#FF0000", "blue"],
            ),
        ),
    )
)
st.altair_chart(chart, use_container_width=True)

st.subheader("Lines and Points, with mean and linear regression")
base = (
    alt.Chart(df.reset_index(), title="Chart Title")
    .mark_point(size=100)
    .encode(
        x=alt.X("x_col", title=None),
        y=alt.Y("y_col", title=None),
    )
)
mean_line = (
    alt.Chart(df.reset_index())
    .mark_rule(color="gray", strokeDash=[6, 2], strokeWidth=1)  # rule not line!
    .encode(
        y="mean(y_col)",
    )
)
reg_line = base.transform_regression("x_col", "y_col").mark_line(
    color="gray", strokeDash=[4, 4], strokeWidth=1
)
chart = base + base.mark_line() + mean_line + reg_line
st.altair_chart(chart, use_container_width=True)  # type: ignore


st.header("Bar Charts")

st.subheader("quick and simple: st.bar_chart for above data")
st.bar_chart(df.reset_index(), x="x_col", y="y_col", x_label="", y_label="")

st.subheader("st.bar_chart with multiple columns")
df = pd.DataFrame(RNG.random((20, 3)), columns=["a", "b", "c"])
st.bar_chart(df, stack=True, horizontal=False)

st.subheader(
    "more advanced and flexible: alt.Chart for time series in long table format"
)

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
df["value"] = RNG.random(len(df))
st.write(df)

# custom color scale
COLOR_SCALE = alt.Scale(
    domain=["group1", "group2"],
    range=["#FF0000", "blue"],
)

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        # date axis, prints month names in English
        # x=alt.X("yearmonth(month):T", title=None),
        # simple print month numbers, preferred when in multi lang context
        x=alt.X("yearmonth(month):T", title=None),
        # alternative:
        # x=alt.X("month:N")
        y=alt.Y("value:Q", title=None),
        color=alt.Color("group:N", scale=COLOR_SCALE),
        xOffset="group:N",  # remove to get stacked bars
        tooltip=[
            alt.Tooltip("yearmonth(month):T", title="Month"),
            alt.Tooltip("group:N", title="Group"),
            alt.Tooltip("value:Q", title="Value"),
        ],
    )
)
st.altair_chart(chart, use_container_width=True)

st.subheader("BarChart for data in wide table format")
# custom color scale
df = pd.DataFrame(
    {
        "month": pd.date_range(start="2023-01", end="2024-12", freq="MS").strftime(
            "%Y-%m"
        )
    }
).set_index("month")
df["col1"] = RNG.random(len(df))
df["col2"] = RNG.random(len(df))
st.write(df)
chart = (
    alt.Chart(df.reset_index())
    # wide table to long table
    .transform_fold(["col1", "col2"], as_=["cols", "kWh"])
    .mark_bar()
    .encode(
        x=alt.X("month:N", title=None),
        y=alt.Y("kWh:Q", title=None),
        color=alt.Color(
            "cols:N",
            scale=alt.Scale(
                domain=["col1", "col2"],
                range=["#FF0000", "blue"],
            ),
        ),
        xOffset="cols:N",
    )
)
st.altair_chart(chart, use_container_width=True)

# :T stands for Temporal. It indicates that the field contains date or time values.
# :N stands for Nominal. It indicates that the field contains categorical data,
#   which represents discrete categories or labels.
# :Q stands for Quantitative. It indicates that the field contains numerical data
#   that can be measured and compared.
