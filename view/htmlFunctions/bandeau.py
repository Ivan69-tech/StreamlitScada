import streamlit as st
from view.backgroundImage import get_base64_of_bin_file



def set_bandeau(png_file):
    img_path = png_file
    img_base64 = get_base64_of_bin_file(img_path)

    st.markdown(
        f"""
        <style>
            .banner {{
                position: relative;
                background: url("data:image/png;base64,{img_base64}") no-repeat center;
                background-size: cover;
                padding: 54px 28px;
                border-radius: 16px;
                text-align: center;
                color: #0f172a;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
                border: 1px solid rgba(15, 23, 42, 0.06);
            }}
            /* Overlay semi-transparent */
            .banner::before {{
                content: "";
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: linear-gradient(180deg, rgba(255,255,255,0.65) 0%, rgba(255,255,255,0.72) 100%);
            }}
            .banner h1, .banner p {{
                position: relative; /* pour passer au-dessus de l’overlay */
                z-index: 1;
            }}
            .banner h1 {{
                font-size: 42px;
                margin: 0;
                letter-spacing: -0.02em;
                line-height: 1.1;
            }}
            .banner p {{
                font-size: 18px;
                margin-top: 12px;
                color: #334155;
            }}
            @media (max-width: 768px) {{
                .banner {{ padding: 36px 18px; border-radius: 12px; }}
                .banner h1 {{ font-size: 28px; }}
                .banner p {{ font-size: 16px; }}
            }}
        </style>

        <div class="banner">
            <h1>Dashboard de contrôle BESS — temps réel</h1>
            <p>Un serveur Modbus tourne en arrière-plan pour simuler un BESS.</p>
            <p>Ce dashboard inclut un client Modbus (un client MQTT aurait aussi été possible).</p>
            <p>Une base de données Postgresql est intégrée pour tracer l'historique des données.</p>
        </div>
        """,
        unsafe_allow_html=True
    )