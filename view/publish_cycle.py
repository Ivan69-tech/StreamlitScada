import streamlit as st
import threading
from mqtt import MqttReader

def publish_cycle():
    if "mqtt_reader" not in st.session_state:
            st.session_state["mqtt_reader"] = MqttReader()

    if "publisher_thread" not in st.session_state:
        lock = threading.Lock()
        with lock:
            if "publisher_thread" not in st.session_state:
                thread = threading.Thread(
                    target=st.session_state["mqtt_reader"].cycle_publish,
                    daemon=True
                )
                st.session_state["publisher_thread"] = thread
                thread.start()