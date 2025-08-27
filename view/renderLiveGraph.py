import streamlit as st
import altair as alt
from modbus import ModbusClient
from controller import SMT
import pandas as pd
from view.component.chart import AltChart
from view.htmlFunctions.center import centerText
from context.context import newContext

def RenderLiveGraph():
    col1, col2, col3 = st.columns(3)

    if "modbus_client" not in st.session_state:
        st.session_state["modbus_client"] = ModbusClient()

    if "smt" not in st.session_state:
        # Ensure context is provided consistently
        st.session_state["smt"] = SMT(newContext())
    
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
            centerText("Watchdog — 10 dernières valeurs")
            AltChart(df_watchdog,0,11, xlabel="X", ylabel="Watchdog value")
                
    with col2:
        if not state:
            st.write("Aucune lecture Modbus …")
        else:
            centerText("State — 10 dernières valeurs")
            AltChart(df_state, xlabel="X", ylabel="State")

        if not Q:
            st.write("Aucune lecture Modbus …")
        else:
            centerText("Q — 10 dernières valeurs")
            AltChart(df_Q, xlabel="X", ylabel="Q value (Var)")

    with col3:
        if not P:
            st.write("Aucune lecture Modbus …")
        else:
            centerText("P — 10 dernières valeurs")
            AltChart(df_P, xlabel="X", ylabel="P value (W)")
            
        
