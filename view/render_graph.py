import streamlit as st
import plotly.express as px
from collections import deque
from mqtt import MqttReader

def publish_msg():
    msg = st.session_state["my_msg"]
    if msg is not None:
        st.session_state["mqtt_reader"].publish_messages(int(msg))
        st.session_state["my_msg"] = None


def render_graph():

    if "my_msg" not in st.session_state:
        st.session_state["my_msg"] = None

    if "messages" not in st.session_state:
        st.session_state["messages"] = deque(maxlen=10)

    if "mqtt_reader" not in st.session_state:
        st.session_state["mqtt_reader"] = MqttReader()
    
    # --- Récupérer nouveaux messages ---
    new_msgs = st.session_state["mqtt_reader"].get_messages()
    for v in new_msgs:
        st.session_state["messages"].append(v)

    Y = list(st.session_state["messages"])
    X = list(range(len(Y)))

    if not Y:
        st.write("En attente de messages MQTT …")
    else:
        st.markdown("**Last 10 MQTT values**")
        fig = px.line(x=X, y=Y, markers=True)
        st.plotly_chart(fig, use_container_width=True)


    st.number_input(
        "Publie un message MQTT",
        key="my_msg",
        value=None,
        placeholder="Tape un nombre...",
        on_change=publish_msg
    )