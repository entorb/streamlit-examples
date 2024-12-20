"""URL parameters get and set."""

import streamlit as st

lst = ["Dpt1", "Dpt2", "Dpt3"]
key = "sel_dpt"
# read url parameter and store as session state
if key in st.query_params:
    st.session_state[key] = st.query_params[key]
if key not in st.session_state:
    idx = 0
else:
    idx = lst.index(st.session_state[key]) if st.session_state[key] in lst else None

sel = st.selectbox(
    label="Select Department",
    options=lst,
    index=idx,
)

# after selection: update url parameter and session state
if sel:
    st.query_params[key] = sel
    st.session_state[key] = sel
