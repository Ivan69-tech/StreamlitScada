import streamlit as st
import altair as alt

def AltChart(df, min=None, max=None, xlabel="x", ylabel="y"):

    if min is not None and max is not None:
        y_encoding = alt.Y(ylabel, scale=alt.Scale(domain=[min, max]))
    else:
        y_encoding = alt.Y(ylabel)

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=xlabel,
            y=y_encoding
        )
        .configure_view(
            strokeWidth=0
        )
        .properties(
            padding={"left": 10, "right": 40, "top": 40, "bottom": 10}
        )
    )

    st.altair_chart(chart, use_container_width=True)
    return
