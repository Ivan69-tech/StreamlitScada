import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import pytz
from view.htmlFunctions.center import centerText

def renderHistorical(db, context):
    centerText("📈 Historique des mesures")

    paris = pytz.timezone("Europe/Paris")

    # --- Initialisation session_state ---
    if "variable" not in st.session_state:
        st.session_state.variable = list(context.keys())[0]
    if "start_datetime" not in st.session_state:
        st.session_state.start_datetime = datetime.now(paris) - timedelta(days=1)
    if "end_datetime" not in st.session_state:
        st.session_state.end_datetime = datetime.now(paris)
    if "show_graph" not in st.session_state:
        st.session_state.show_graph = False

    # --- Sélecteur de variable ---
    _,col1,_ = st.columns([1,5,1,])
    
    with col1:
        st.selectbox(
        "Choisissez une variable :", 
        list(context.keys()), 
        index=list(context.keys()).index(st.session_state.variable),
        key="variable"
    )

    # --- Sélecteurs de dates ---
    _,col1,col2,_ = st.columns([1,3,3,1])
    with col1:
        start_date = st.date_input("Date de début", st.session_state.start_datetime.date())
        start_time = st.time_input("Heure de début", st.session_state.start_datetime.time())
    with col2:
        end_date = st.date_input("Date de fin", st.session_state.end_datetime.date())
        end_time = st.time_input("Heure de fin", st.session_state.end_datetime.time())

    # Combine et garde timezone Europe/Paris
    st.session_state.start_datetime = paris.localize(datetime.combine(start_date, start_time))
    st.session_state.end_datetime = paris.localize(datetime.combine(end_date, end_time))

    # --- Bouton tracer ---
    if st.button("Tracer"):
        st.session_state.show_graph = True

    # --- Affichage du graphe si demandé ---
    if st.session_state.show_graph:
        # Conversion des bornes vers UTC pour la requête
        start_utc = st.session_state.start_datetime.astimezone(pytz.UTC)
        end_utc = st.session_state.end_datetime.astimezone(pytz.UTC)

        query = f"""
            SELECT timestamp, {st.session_state.variable}
            FROM context
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        """
        rows = db.execute_query(query, (start_utc, end_utc))

        if not rows:
            st.warning("⚠️ Aucune donnée trouvée pour cette période.")
            return

        df = pd.DataFrame(rows, columns=["timestamp", st.session_state.variable])
        # Conversion UTC -> Europe/Paris pour affichage
        df["timestamp"] = (
            pd.to_datetime(df["timestamp"], utc=True)
            .dt.tz_convert("Europe/Paris")
            .dt.tz_localize(None)  # enlève le +02:00
        )

        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "timestamp:T",
                    axis=alt.Axis(format="%Hh%M:%S")  # Format 24h : ex. "22h00"
                ),
                y=alt.Y(
                    f"{st.session_state.variable}:Q",
                    title=st.session_state.variable
                ),
                tooltip=["timestamp:T", f"{st.session_state.variable}:Q"]
            )
            .properties(
                width=700,
                height=400,
                title=f"Évolution de {st.session_state.variable}",
                background="white"
            )
            .configure_view(
                strokeWidth=0, 
                fill="white"         # <- fond de la zone de tracé
            )
        )

        st.altair_chart(chart, use_container_width=True)


        _,col1,_ = st.columns([3,3,3])
        with col1:
            st.dataframe(df)
