"""Intro."""  # noqa: N999

import streamlit as st

from helper import get_logger_from_filename

logger = get_logger_from_filename(__file__)

st.title(__doc__[:-1])  # type: ignore

st.header("Python Streamlit is more fun than PowerBI and PowerPoint :smirk:)")

st.markdown("""
*"Streamlit is an open-source Python framework for data scientists and AI/ML engineers to deliver interactive data apps - in only a few lines of code."*
""")  # noqa: E501


st.header("Pros")
cols = st.columns(2)
cols[0].markdown("""
### Python
- Most prominent language in the world
- Open Source
- GitHub Copilot "speaks" Python fluently
- Reuse of code
- Unit tests
  - All pages open without errors
  - Simulate user interactions
### Cost-Effective
- No costs besides server hosting
- No DB needed
### Performance
- Great performance thanks to easy caching
- Very little overhead
- Full control of database queries, so access to prod database is feasible
""")

cols[1].markdown("""
### Versatile
- Standalone Web-Application (Backend + Frontend)
- Easy to create multi-language apps using a translation map
- Authentication via Azure etc. possible
- Access to Databases
- Access to APIs
- Parse or generate files
- Perform advanced calculations, e.g., via machine learning (AI)
- Generate image files
### User Interface
- Ships with light and dark themes
- Markdown support for fast and simple text composition
- LaTeX support for mathematical expressions
""")


st.header("Cons")
cols = st.columns(2)
cols[0].markdown("""
### Neutral Points
- Requires Python knowledge
- Limited design and layout options, leading to less time spent on layout
""")

cols[1].markdown("""
### Cons
- Streamlit is stateful, so deployment to kubernetes is not straightforward
- Requires deployment know-how
- Implementing simple reports in PowerBI is faster
- Pages are static; user interaction is required for refresh (there might be workarounds)
""")  # noqa: E501
