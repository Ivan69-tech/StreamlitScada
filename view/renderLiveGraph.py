import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from modbus import ModbusClient
from controller import SMT



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
    X1 = list(range(len(watchdog)))
    X2 = list(range(len(state)))
    X3 = list(range(len(P)))
    X4 = list(range(len(Q)))

    with col1 :
        if not watchdog:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 watchdog values**")
            fig = px.line(x=X1, y=watchdog, markers=True)
            fig.update_yaxes(range=[0, 11])
            st.plotly_chart(fig, use_container_width=True, key="watchdog_chart")


    with col2 :
        if not state:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 State values**")
            fig = px.line(x=X2, y=state, markers=True)
            st.plotly_chart(fig, use_container_width=True, key="state_chart")

    with col3 :
        if not P:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 P values**")
            fig = px.line(x=X3, y=P, markers=True)
            st.plotly_chart(fig, use_container_width=True, key="P_chart")

        if not Q:
            st.write("Aucune lecture Modbus …")
        else:
            st.markdown("**Last 10 Q values**")
            fig = px.line(x=X4, y=Q, markers=True)
            st.plotly_chart(fig, use_container_width=True, key="Q_chart")

