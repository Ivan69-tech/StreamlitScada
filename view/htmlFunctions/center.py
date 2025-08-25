import streamlit as st

def centerText(text) :
    return st.markdown(f"<div style='text-align: center; font-weight: bold;'>" + text + "</div>",
            unsafe_allow_html=True)