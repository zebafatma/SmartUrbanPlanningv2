"""
Dashboard Page

Displays AI prediction statistics and
external urban analytics.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.recommendation.context_builder import ContextBuilder

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Urban Analytics Dashboard")

# ==========================================================
# Check Analysis
# ==========================================================

if "analysis" not in st.session_state:

    st.warning("Please analyze an image first.")

    st.stop()

analysis = st.session_state["analysis"]

statistics = analysis["statistics"]

area = st.session_state["area"]

ward = st.session_state["ward"]

# ==========================================================
# Build Urban Context
# ==========================================================

builder = ContextBuilder()

context = builder.build(
    segmentation_statistics=statistics,
    area_name=area,
    ward_name=ward,
)

# ==========================================================
# KPI Cards
# ==========================================================

st.header("Land Cover Distribution")

percentages = statistics["percentages"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🛣 Roads",
    f"{percentages['Road']} %",
)

col2.metric(
    "🏢 Buildings",
    f"{percentages['Building']} %",
)

col3.metric(
    "🌳 Vegetation",
    f"{percentages['Vegetation']} %",
)

col4.metric(
    "💧 Water",
    f"{percentages['Water']} %",
)

st.divider()

# ==========================================================
# Charts
# ==========================================================

chart_data = pd.DataFrame(
    {
        "Class": [
            "Road",
            "Building",
            "Vegetation",
            "Water",
            "Background",
        ],
        "Percentage": [
            percentages["Road"],
            percentages["Building"],
            percentages["Vegetation"],
            percentages["Water"],
            percentages["Background"],
        ],
    }
)

left, right = st.columns(2)

with left:

    st.subheader("Land Cover Distribution")

    pie = px.pie(
        chart_data,
        values="Percentage",
        names="Class",
        hole=0.45,
    )

    st.plotly_chart(
        pie,
        use_container_width=True,
    )

with right:

    st.subheader("Area Coverage")

    bar = px.bar(
        chart_data,
        x="Class",
        y="Percentage",
        text="Percentage",
    )

    st.plotly_chart(
        bar,
        use_container_width=True,
    )

st.divider()

# ==========================================================
# External Data
# ==========================================================

st.header("Urban Information")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🚦 Traffic",
        "👥 Population",
        "🌦 Weather",
        "🚨 Accidents",
    ]
)

# ----------------------------------------------------------

with tab1:

    traffic = context.traffic

    st.metric(
        "Traffic Category",
        traffic.traffic_category,
    )

    st.metric(
        "Traffic Score",
        traffic.traffic_score,
    )

    st.metric(
        "Average Speed",
        f"{traffic.average_speed:.2f} km/h",
    )

    st.metric(
        "Traffic Volume",
        traffic.traffic_volume,
    )

# ----------------------------------------------------------

with tab2:

    population = context.population

    st.metric(
        "Population",
        population.population,
    )

    st.metric(
        "Population Density",
        population.population_density,
    )

    st.metric(
        "Population Category",
        population.population_category,
    )

    st.metric(
        "Infrastructure Score",
        population.infrastructure_score,
    )

# ----------------------------------------------------------

with tab3:

    weather = context.weather

    st.metric(
        "Average Temperature",
        f"{weather.average_temperature} °C",
    )

    st.metric(
        "Rainfall",
        weather.rainfall,
    )

    st.metric(
        "Weather",
        weather.weather_category,
    )

    st.metric(
        "Heat Risk",
        weather.heat_risk,
    )

# ----------------------------------------------------------

with tab4:

    accidents = context.accidents

    st.metric(
        "Safety Category",
        accidents.safety_category,
    )

    st.metric(
        "Total Accidents",
        accidents.total_accidents,
    )

    st.metric(
        "Fatal Accidents",
        accidents.fatal_accidents,
    )

    st.metric(
        "Severity Index",
        accidents.accident_severity_index,
    )

st.divider()

# ==========================================================
# Statistics Table
# ==========================================================

st.header("Detailed Statistics")

pixel_counts = statistics["pixel_counts"]

table = pd.DataFrame(
    {
        "Land Cover": pixel_counts.keys(),
        "Pixels": pixel_counts.values(),
    }
)

st.dataframe(
    table,
    use_container_width=True,
)
