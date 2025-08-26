import streamlit as st
from streamlit_autorefresh import st_autorefresh
from view.publish_cycle import publish_cycle
from view.render_title import render_title
from view.renderLiveGraph import RenderLiveGraph
from view.renderControl import RenderControl
from view.htmlFunctions.bandeau import set_bandeau
import plotly.express as px
from controller import SMT



# --- Page config & global theme (visual only) ---
st.set_page_config(page_title="BESS Control Dashboard", page_icon="🔋", layout="wide")

# Inject light modern theme CSS (no functional changes)
st.markdown(
    """
    <style>
      :root {
        --accent: #4f46e5;
        --accent-2: #06b6d4;
        --bg-soft: #0b1220;
        --card-bg: rgba(255,255,255,0.65);
        --text-strong: #0f172a;
      }
      /* App background */
      [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
      }
      /* Make default containers look like cards */
      section.main > div {
        gap: 0.75rem;
      }
      .stApp header { backdrop-filter: blur(6px); }
      .stMarkdown, .stText, .stDataFrame {
        color: var(--text-strong);
      }
      /* Buttons */
      .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        color: white;
        border: 0;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        box-shadow: 0 6px 20px rgba(79,70,229,0.25);
        transition: transform .05s ease-in-out, box-shadow .2s ease;
      }
      .stButton > button:hover { transform: translateY(-1px); }
      .stButton > button:active { transform: translateY(0); }
      /* Inputs */
      div[data-baseweb="input"] input {
        border-radius: 10px;
        font-size: 18px;
        padding: 10px 12px;
      }
      /* Also bump font size for selects/textareas if present */
      div[data-baseweb="select"] div, textarea {
        font-size: 18px;
      }
      label p { font-weight: 600; font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Auto-refresh ---
st_autorefresh(interval=1000, limit=None, key="count")

# --- thread for watchdog ---
publish_cycle()

# --- handle title ---
render_title()

# --- lire à chaque cycle ---
st.session_state.smt.checkConnection()
st.session_state.smt.Read()

set_bandeau("view/images/BESS.png")
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













