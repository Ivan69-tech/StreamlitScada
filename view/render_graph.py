import streamlit as st
import plotly.express as px
from collections import deque
from modbus import ModbusClient
from controller import SMT


def RenderGraph():


    if "modbus_client" not in st.session_state:
        st.session_state["modbus_client"] = ModbusClient()

    if "smt" not in st.session_state:
        st.session_state["smt"] = SMT()
    
    # --- lire à nouveau ---
    st.session_state.smt.Read()

    Y =  st.session_state.smt.watchdog
    X = list(range(len(Y)))

    if not Y:
        st.write("Aucune lecture Modbus …")
    else:
        st.markdown("**Last 10 Modbus values**")
        fig = px.line(x=X, y=Y, markers=True)
        st.plotly_chart(fig, use_container_width=True)
