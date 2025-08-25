import streamlit as st
import plotly.graph_objects as go

def BackgroundContainer(fig):
    with st.container():
        st.markdown(
            """
            <style>
            .white-container {
                background-color: white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Graphe dans un div avec la classe CSS
        placeholder = st.empty()
        placeholder.markdown('<div class="white-container">', unsafe_allow_html=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        placeholder.markdown('</div>', unsafe_allow_html=True)
        return
