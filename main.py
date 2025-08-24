import streamlit as st
from collections import deque
from streamlit_autorefresh import st_autorefresh
from mqtt import MqttReader
from view.publish_cycle import publish_cycle
from view.render_graph import render_graph
from view.render_title import render_title



# --- Auto-refresh ---
st_autorefresh(interval=1000, limit=None, key="count")

# --- thread to publish to mqtt broker ping/ping ---
publish_cycle()

# --- handle title ---
render_title()

# --- handle graph ---
col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    render_graph()











