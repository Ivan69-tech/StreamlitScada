import streamlit as st
import threading
from controller import SMT

def publish_cycle():
    if "smt" not in st.session_state:
            st.session_state["smt"] = SMT()

    if "publisher_thread" not in st.session_state or not st.session_state["publisher_thread"].is_alive():
        thread = threading.Thread(
            target=st.session_state["smt"].Watchdog,
            daemon=True
        )
        thread.start()
        st.session_state["publisher_thread"] = thread