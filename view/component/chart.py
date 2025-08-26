import streamlit as st
import altair as alt

def AltChart(df, min=None, max=None, xlabel="x", ylabel="y"):

    if min is not None and max is not None:
        y_encoding = alt.Y(ylabel, scale=alt.Scale(domain=[min, max]))
    else:
        y_encoding = alt.Y(ylabel)

    base = alt.Chart(df)
    line = base.mark_line(point=True, strokeWidth=2, color="#4f46e5").encode(
        x=alt.X(xlabel, title=""),
        y=y_encoding,
        tooltip=[xlabel, ylabel]
    )

    chart = (
        line
        .configure_view(strokeWidth=0)
        .configure_axis(
            grid=True,
            gridColor="#e5e7eb",
            labelColor="#334155",
            titleColor="#0f172a"
        )
        .configure_point(size=60, color="#06b6d4")
        .properties(padding={"left": 10, "right": 16, "top": 10, "bottom": 10})
    )

    st.altair_chart(chart, use_container_width=True)
    return
