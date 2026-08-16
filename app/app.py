"""
Smart Urban Planning System

Main Streamlit Application.
"""

import streamlit as st

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Smart Urban Planning",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# Title
# =====================================================

st.title("🌍 Smart Urban Planning using AI")

st.markdown("""
Artificial Intelligence based Urban Planning System

Built using

- Semantic Segmentation
- Satellite Imagery
- Traffic Analysis
- Population Analysis
- Weather Analysis
- Urban Recommendation Engine
""")

st.divider()

# =====================================================
# Project Workflow
# =====================================================

st.header("Project Workflow")

st.markdown("""

1. Upload Satellite Image

2. AI detects

   - Roads
   - Buildings
   - Vegetation
   - Water Bodies

3. External datasets are analysed

   - Traffic
   - Population
   - Weather
   - Road Accidents
   - Public Amenities

4. AI generates Urban Planning Recommendations

""")

st.success("Use the navigation menu on the left to start the analysis.")
