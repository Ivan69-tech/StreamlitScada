import streamlit as st
import altair as alt
from modbus import ModbusClient
from controller import SMT
import pandas as pd


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
            chart = alt.Chart(df_watchdog).mark_line(point=True).encode(
                x="x",
                y=alt.Y("y", scale=alt.Scale(domain=[0, 11]))
            )
            st.altair_chart(chart, use_container_width=True)

    with col2:
        if not state:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 State values**")
            chart = alt.Chart(df_state).mark_line(point=True).encode(
                x="x",
                y="y"
            )
            st.altair_chart(chart, use_container_width=True)

    with col3:
        if not P:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 P values**")
            chart = alt.Chart(df_P).mark_line(point=True).encode(
                x="x",
                y="y"
            )
            st.altair_chart(chart, use_container_width=True)

        if not Q:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 Q values**")
            chart = alt.Chart(df_Q).mark_line(point=True).encode(
                x="x",
                y="y"
            )
            st.altair_chart(chart, use_container_width=True)
