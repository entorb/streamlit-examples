"""Sections and Text."""

import streamlit as st

from helper import filename_to_title, get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(filename_to_title(__file__))


st.header("Columns")
st.subheader("3 same size columns")

DUMMY_TEXT = """This is a long plain dummy text. This is a long plain dummy text. This is a long plain dummy text. This is a long plain dummy text."""  # noqa: E501

cols = st.columns(3)
cols[0].subheader("Col1")
cols[0].write(DUMMY_TEXT)
cols[1].subheader("Col2")
cols[1].write(DUMMY_TEXT)
cols[2].subheader("Col3")
cols[2].write(DUMMY_TEXT)

st.subheader("1/3 and 2/3 columns with only the first used")
cols = st.columns((1, 2))  # 1/3 and 2/3 columns
cols[0].subheader("Col1")
cols[0].write(DUMMY_TEXT)


st.header("Text")
cols = st.columns(2)
cols[0].subheader("Plain Text")
cols[0].write(DUMMY_TEXT)


cols[1].subheader("Markdown")
cols[1].markdown("""
This is a markdown text with **bold**,
*italics*, `code`, [link](https://streamlit.io).
""")

st.columns(1)

st.subheader("Code")
cols = st.columns(3)

s = """# Some comment
print("Hello, world!")
"""
cols[0].write("Plain format")
cols[0].code(s, language=None)
cols[1].write("Python highlighting")
cols[1].code(s, language="python")
cols[2].write("CSV")
cols[2].code("Column 1,Column 2\n12.3,23.4", language="csv")


st.subheader("LaTeX")
# 2 equals 1
cols = st.columns(2)
cols[0].latex(r"""
\begin{align}
a &= b\\
a^2 &= ab\\
2 a^2 &= a^2 + ab\\
2 a^2 -2ab &= a^2 - ab\\
2 a (a-b) &= a (a-b)\\
2 a &= a \\
2 &= 1 \\
\end{align}
""")

# Maxwell equations
cols[1].latex(r"""
\begin{align}
\nabla \cdot \vec{E} & = \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \vec{B} & = 0 \\
\nabla \times \vec{E} & = -\frac{\partial \vec{B}}{\partial t} \\
\nabla \times \vec{B} & = \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t}
\end{align}
""")  # noqa: E501


# st.header("Dark Layout Toggle")
# toggle_dark = st.toggle("Dark Layout", value=True)
# if st.get_option("theme.base") == "light" and toggle_dark:
#     st._config.set_option("theme.base", "dark")  # type: ignore
#     st.rerun()
# elif st.get_option("theme.base") == "dark" and not toggle_dark:
#     st._config.set_option("theme.base", "light")  # type: ignore
#     st.rerun()
