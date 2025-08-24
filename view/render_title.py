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

    st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100vw;
    }
    </style>
    """,
    unsafe_allow_html=True
)