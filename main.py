import streamlit as st
from streamlit_autorefresh import st_autorefresh
from view.publish_cycle import publish_cycle
from view.render_title import render_title
from view.renderLiveGraph import RenderLiveGraph
from view.renderControl import RenderControl
from view.renderHistorical import renderHistorical
from view.htmlFunctions.bandeau import set_bandeau
from view.htmlFunctions.generalStyle import generalStyle
from dotenv import load_dotenv
from context.context import newContext
from controller import SMT
from datetime import datetime






load_dotenv()




# --- Auto-refresh ---
st_autorefresh(interval=1000, limit=None, key="count")

generalStyle()

# --- handle title ---
render_title()


print(datetime.now())

if "smt" not in st.session_state:
        st.session_state["smt"] = SMT(newContext())


# --- lire à chaque cycle (protégé) ---
try:
    st.session_state.smt.check_connection()
    st.session_state.smt.check_db_connection()
    st.session_state.smt.read()
    st.session_state.smt.watchdog_cycle()
except Exception as e:
    st.error(f"Erreur lors de l'exécution du cycle : {str(e)}")
    print(f"Erreur cycle: {e}")

set_bandeau("view/images/BESS.png")
# --- handle graph ---
tab1, tab2, tab3 = st.tabs(["⚙️ Commandes", "📊 Graphiques temps réel", "📈 Historique des mesures"])

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

with tab3:
    if not st.session_state.smt.db_connected :
        st.markdown("**Connexion avec la base de donnée impossible**")
        st.session_state.smt.db.connect()
    else :
        renderHistorical(st.session_state.smt.db, st.session_state.smt.context.context)













