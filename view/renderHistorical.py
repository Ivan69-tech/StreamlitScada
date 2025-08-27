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
    
    # AJOUT : Nettoyage automatique des anciennes données
    if "graph_data" in st.session_state:
        del st.session_state.graph_data
    
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
    
    # AJOUT : Validation de la plage de dates
    time_diff = st.session_state.end_datetime - st.session_state.start_datetime
    if time_diff.days > 7:
        st.warning("⚠️ Période limitée à 7 jours maximum pour éviter les problèmes de performance.")
        return
    
    # --- Bouton tracer ---
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Tracer"):
            st.session_state.show_graph = True
    with col2:
        if st.button("Effacer"):
            st.session_state.show_graph = False
            if "graph_data" in st.session_state:
                del st.session_state.graph_data
            st.rerun()
    
    # --- Affichage du graphe si demandé ---
    if st.session_state.show_graph:
        # Conversion des bornes vers UTC pour la requête
        start_utc = st.session_state.start_datetime.astimezone(pytz.UTC)
        end_utc = st.session_state.end_datetime.astimezone(pytz.UTC)
        
        # AJOUT : Limitation du nombre de points
        query = f"""
        SELECT timestamp, {st.session_state.variable}
        FROM context
        WHERE timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC
        LIMIT 1000
        """
        
        with st.spinner("Chargement des données..."):
            rows = db.execute_query(query, (start_utc, end_utc))
        
        if not rows:
            st.warning("⚠️ Aucune donnée trouvée pour cette période.")
            return
        
        # MODIF : Ne pas stocker le DataFrame dans session_state
        df = pd.DataFrame(rows, columns=["timestamp", st.session_state.variable])
        
        # Conversion UTC -> Europe/Paris pour affichage
        df["timestamp"] = (
            pd.to_datetime(df["timestamp"], utc=True)
            .dt.tz_convert("Europe/Paris")
            .dt.tz_localize(None)
        )
        
        # AJOUT : Information sur le nombre de points
        st.info(f"📊 {len(df)} points de données chargés")
        
        # MODIF : Simplification du graphique pour de meilleures performances
        chart = (
            alt.Chart(df)
            .mark_line()  # Retirer point=True pour de meilleures performances
            .encode(
                x=alt.X(
                    "timestamp:T",
                    axis=alt.Axis(format="%Hh%M")
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
                title=f"Évolution de {st.session_state.variable}"
            )
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # MODIF : Affichage limité du dataframe
        _,col1,_ = st.columns([3,3,3])
        with col1:
            if len(df) > 1000:
                st.write("Échantillon des données (premières 100 lignes) :")
                st.dataframe(df.head(100))
            else:
                st.dataframe(df)