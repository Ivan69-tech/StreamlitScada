import streamlit as st

def centerText(text) :
    return st.markdown(
        f"<div style='text-align: center; font-weight: 600; font-size: 1.05rem; color: #0f172a; padding: 8px 0;'>"
        + text + "</div>",
        unsafe_allow_html=True
    )