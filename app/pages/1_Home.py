"""
Home Page

Smart Urban Planning using AI
"""

import streamlit as st

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
)

# ==========================================================
# Header
# ==========================================================

st.title("🏙️ Smart Urban Planning using Artificial Intelligence")

st.markdown("""
### AI-powered Decision Support System for Sustainable Urban Development

This platform combines **Deep Learning**, **Satellite Image Segmentation**,
and **Urban Analytics** to assist planners in making informed decisions.
""")

st.divider()

# ==========================================================
# About
# ==========================================================

st.header("📖 About the Project")

st.write("""
Smart Urban Planning is an AI-based system that analyzes satellite imagery
to identify different land-cover classes and combines them with
city-specific datasets to generate urban planning recommendations.

The system detects:

- 🛣 Roads
- 🏢 Buildings
- 🌳 Vegetation
- 💧 Water Bodies

It further integrates:

- 🚦 Traffic
- 👥 Population
- 🌦 Weather
- 🚑 Accident Statistics
- 🏥 Public Amenities

to generate intelligent planning suggestions.
""")

st.divider()

# ==========================================================
# Workflow
# ==========================================================

st.header("⚙️ System Workflow")

st.markdown("""
1. Upload Satellite Image

2. AI performs Semantic Segmentation

3. Land Cover Statistics are generated

4. External datasets are analyzed

5. AI Recommendation Engine evaluates the area

6. Urban Planning Report is generated
""")

st.divider()

# ==========================================================
# Features
# ==========================================================

st.header("✨ Key Features")

col1, col2 = st.columns(2)

with col1:

    st.success("🛰 Satellite Image Segmentation")

    st.success("🌳 Land Cover Detection")

    st.success("📊 Area Statistics")

    st.success("🚦 Traffic Analysis")

with col2:

    st.success("🌦 Weather Analysis")

    st.success("👥 Population Analysis")

    st.success("💡 Urban Recommendations")

    st.success("📄 Report Generation")

st.divider()

# ==========================================================
# Technologies
# ==========================================================

st.header("🛠 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:

    st.subheader("AI")

    st.write("""
- TensorFlow
- Attention ResUNet
- OpenEarthMap
- Albumentations
""")

with tech2:

    st.subheader("Backend Logic")

    st.write("""
- Python
- GeoPandas
- OpenCV
- Pandas
""")

with tech3:

    st.subheader("Frontend")

    st.write("""
- Streamlit
- Plotly
- Folium
""")

st.divider()

# ==========================================================
# Dataset Summary
# ==========================================================

st.header("📂 Datasets")

dataset1, dataset2, dataset3 = st.columns(3)

dataset1.metric(
    "Segmentation Dataset",
    "OpenEarthMap",
)

dataset2.metric(
    "Traffic Dataset",
    "Bengaluru",
)

dataset3.metric(
    "Population Dataset",
    "BBMP",
)

dataset4, dataset5, dataset6 = st.columns(3)

dataset4.metric(
    "Weather",
    "NASA POWER",
)

dataset5.metric(
    "Accidents",
    "OpenCity",
)

dataset6.metric(
    "Amenities",
    "OpenStreetMap",
)

st.divider()

# ==========================================================
# Start
# ==========================================================

st.info("👈 Use the sidebar to start the analysis.")
