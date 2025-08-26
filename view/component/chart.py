import streamlit as st
import altair as alt

def AltChart(df, min=None, max=None, xlabel="x", ylabel="y"):

    if min is not None and max is not None:
        y_encoding = alt.Y("y", scale=alt.Scale(domain=[min, max]), title=ylabel)
    else:
        y_encoding = alt.Y("y", title=ylabel)

    base = alt.Chart(df)
    line = base.mark_line(point=True, strokeWidth=2, color="#4f46e5").encode(
        x=alt.X("x", title=xlabel),
        y=y_encoding,
        tooltip=[alt.Tooltip("x", title=xlabel), alt.Tooltip("y", title=ylabel)]
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
        .properties(padding={"left": 20, "right": 20, "top": 20, "bottom": 20})
    )

    st.altair_chart(chart, use_container_width=True)
    return
