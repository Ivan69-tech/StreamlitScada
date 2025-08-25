import streamlit as st
from streamlit_autorefresh import st_autorefresh
from view.publish_cycle import publish_cycle
from view.render_title import render_title
from view.renderLiveGraph import RenderLiveGraph
from view.renderControl import RenderControl
import plotly.express as px
from controller import SMT



# --- Auto-refresh ---
st_autorefresh(interval=1000, limit=None, key="count")

# --- thread for watchdog ---
publish_cycle()

# --- handle title ---
render_title()

# --- lire à chaque cycle ---
st.session_state.smt.checkConnection()
st.session_state.smt.Read()





# --- handle graph ---
tab1, tab2 = st.tabs(["⚙️ Commandes", "📊 Graphiques temps réel"])

with tab1:
    if not st.session_state.smt.connected :
        st.markdown("**Connexion avec le serveur modbus impossible**")
    else :
        RenderControl()

with tab2:
    if not st.session_state.smt.connected :
        st.markdown("**Connexion avec le serveur modbus impossible**")
    else :
        RenderLiveGraph()













