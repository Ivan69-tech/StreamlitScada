import streamlit as st
import altair as alt
from modbus import ModbusClient
from controller import SMT
import pandas as pd
from view.component.chart import AltChart

def RenderLiveGraph():
    col1, col2, col3 = st.columns(3)

    if "modbus_client" not in st.session_state:
        st.session_state["modbus_client"] = ModbusClient()

    if "smt" not in st.session_state:
        st.session_state["smt"] = SMT()
    
    watchdog =  st.session_state.smt.watchdog
    state = st.session_state.smt.state
    P = st.session_state.smt.P_kW
    Q = st.session_state.smt.Q_kVar
    soc = st.session_state.smt.soc

    # Création des DataFrames pour Altair
    df_watchdog = pd.DataFrame({"x": range(len(watchdog)), "y": watchdog})
    df_state = pd.DataFrame({"x": range(len(state)), "y": state})
    df_P = pd.DataFrame({"x": range(len(P)), "y": P})
    df_Q = pd.DataFrame({"x": range(len(Q)), "y": Q})

    with col1:
        if not watchdog:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 watchdog values**")
            AltChart(df_watchdog,0,11)
                
    with col2:
        if not state:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 State values**")
            AltChart(df_state)

    with col3:
        if not P:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 P values**")
            AltChart(df_P)
            
        if not Q:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 Q values**")
            AltChart(df_Q)
