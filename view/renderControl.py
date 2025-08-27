import streamlit as st
import plotly.express as px
from modbus import ModbusClient
from controller import SMT
from view.htmlFunctions.center import centerText
import pandas as pd
from context.context import newContext


def setP():
    if "P" not in st.session_state:
        st.session_state["P"] = None

    P = st.session_state["P"]
    if P is not None:
        st.session_state["smt"].set_P(int(P))
        st.session_state["P"] = None

def setQ():
    if "Q" not in st.session_state:
        st.session_state["Q"] = None

    Q = st.session_state["Q"]
    if Q is not None:
        st.session_state["smt"].set_Q(int(Q))
        st.session_state["Q"] = None


def RenderControl():

    col1, col2, col3 = st.columns(3)

    if "modbus_client" not in st.session_state:
        st.session_state["modbus_client"] = ModbusClient()

    if "smt" not in st.session_state:
        st.session_state["smt"] = SMT(newContext())

    st.session_state["smt"].check_connection()

    with col1 :
        with st.container() :
            centerText("Contrôles")
            if st.button("Start Bess", use_container_width=True) :
                st.session_state["smt"].start_bess()

            if st.button("Stop Bess", use_container_width=True) :
                st.session_state["smt"].shutdown_bess()

            if st.button("Clear Faults", use_container_width=True) :
                st.session_state["smt"].clear_faults()

            centerText("Consigne de puissance active")
            st.number_input(
                "   ",
                key="P",
                value=None,
                placeholder="Active Power (W)",
                on_change=setP
            )

            centerText("Consigne de puissance réactive")
            st.number_input(
                "   ",
                key="Q",
                value=None,
                placeholder="Reactive power (Var)",
                on_change=setQ
            )

    with col2 :
        try :
            centerText("Statut")
            soc = st.session_state.smt.soc[-1]
            Px = st.session_state.smt.P_kW[-1]
            Qx = st.session_state.smt.Q_kVar[-1]
            centerText(f"State of Charge : {soc}% 🔋")
            centerText(f"Bess Active Power : {Px/1000} kW")
            centerText(f"Bess Reactive Power : {Qx/1000} kVar")
        except :
            st.markdown("**Connexion avec le serveur modbus impossible**")

    with col3 :
        try :
            centerText("Lecture instantanée")
            values = {
                "Watchdog": [st.session_state.smt.watchdog[-1]],
                "State": [st.session_state.smt.state[-1]],
                "P (kW)": [st.session_state.smt.P_kW[-1]/1000],
                "Q (kVar)": [st.session_state.smt.Q_kVar[-1]/1000],
                "SOC (%)": [st.session_state.smt.soc[-1]],
            }

            df = pd.DataFrame(values)
            st.dataframe(df, use_container_width=True)
        except :
            st.markdown("**Connexion avec le serveur modbus impossible**")


        

