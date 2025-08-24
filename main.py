import streamlit as st
from streamlit_autorefresh import st_autorefresh
from view.publish_cycle import publish_cycle
from view.render_title import render_title
from view.renderSMT import RenderSMT
import plotly.express as px
from modbus import ModbusClient
from controller import SMT



# --- Auto-refresh ---
st_autorefresh(interval=1000, limit=None, key="count")

# --- thread to publish to mqtt broker ping/ping ---
publish_cycle()

# --- handle title ---
render_title()

# --- handle graph ---
RenderSMT()












