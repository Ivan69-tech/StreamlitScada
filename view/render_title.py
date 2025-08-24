import streamlit as st

def render_title():
    st.markdown(
        """
        <style>
        /* Cacher le menu hamburger en haut à droite */
        #MainMenu {visibility: hidden;}

        /* Cacher le footer “Made with Streamlit” */
        footer {visibility: hidden;}

        /* Facultatif : cacher le header Streamlit */
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )