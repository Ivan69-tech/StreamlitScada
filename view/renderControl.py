import streamlit as st
import plotly.express as px
from modbus import ModbusClient
from controller import SMT
from view.htmlFunctions.center import centerText
import pandas as pd
from view.backgroundImage import set_png_as_page_bg


def setP():
    if "P" not in st.session_state:
        st.session_state["P"] = None

    P = st.session_state["P"]
    if P is not None:
        st.session_state["smt"].SetP(int(P))
        st.session_state["P"] = None

def setQ():
    if "Q" not in st.session_state:
        st.session_state["Q"] = None

    Q = st.session_state["Q"]
    if Q is not None:
        st.session_state["smt"].SetQ(int(Q))
        st.session_state["Q"] = None


def RenderControl():

    set_png_as_page_bg('view/images/BESS.png')

    col1, col2, col3 = st.columns(3)

    if "modbus_client" not in st.session_state:
        st.session_state["modbus_client"] = ModbusClient()

    if "smt" not in st.session_state:
        st.session_state["smt"] = SMT()

    st.session_state["smt"].checkConnection()

    with col1 :
        with st.container() :
            if st.button("Start Bess", use_container_width=True) :
                st.session_state["smt"].StartBess()

            if st.button("Stop Bess", use_container_width=True) :
                st.session_state["smt"].ShutDownBess()

            if st.button("Clear Faults", use_container_width=True) :
                st.session_state["smt"].ClearFaults()

            st.number_input(
                "Set Active Power setpoint",
                key="P",
                value=None,
                placeholder="Active Power setpoint (W)",
                on_change=setP
            )

            st.number_input(
                "Set Reactive Power setpoint",
                key="Q",
                value=None,
                placeholder="Reactive power setpoint (Var)",
                on_change=setQ
            )

    with col2 :
        try :
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


        

