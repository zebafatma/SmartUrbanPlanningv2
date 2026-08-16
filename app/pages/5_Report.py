"""
Report Page

Generates the final Urban Planning Report.
"""

import json
from datetime import datetime

import streamlit as st

from backend.recommendation.context_builder import ContextBuilder
from backend.recommendation.engine import RecommendationEngine

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Urban Report",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Urban Planning Report")

# ==========================================================
# Validation
# ==========================================================

if "analysis" not in st.session_state:

    st.warning("Please analyze an image first.")

    st.stop()

analysis = st.session_state["analysis"]

statistics = analysis["statistics"]

area = st.session_state["area"]

ward = st.session_state["ward"]

# ==========================================================
# Build Context
# ==========================================================

builder = ContextBuilder()

context = builder.build(
    segmentation_statistics=statistics,
    area_name=area,
    ward_name=ward,
)

engine = RecommendationEngine()

recommendations = engine.generate(context)

# ==========================================================
# Images
# ==========================================================

st.header("Prediction Results")

col1, col2 = st.columns(2)

with col1:

    st.image(
        analysis["original_image"],
        caption="Original Image",
        use_container_width=True,
    )

with col2:

    st.image(
        analysis["overlay_image"],
        caption="Segmentation Overlay",
        use_container_width=True,
    )

st.image(
    analysis["colored_mask"],
    caption="Predicted Segmentation",
    use_container_width=True,
)

st.divider()

# ==========================================================
# Statistics
# ==========================================================

st.header("Land Cover Statistics")

st.json(
    statistics,
    expanded=True,
)

st.divider()

# ==========================================================
# Recommendations
# ==========================================================

st.header("AI Recommendations")

for recommendation in recommendations:

    st.markdown(f"""
### {recommendation.title}

**Priority:** {recommendation.priority}

**Category:** {recommendation.category}

{recommendation.description}

---
""")

# ==========================================================
# Report JSON
# ==========================================================

report = {
    "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "area": area,
    "ward": ward,
    "statistics": statistics,
    "traffic": context.traffic.__dict__,
    "population": context.population.__dict__,
    "weather": context.weather.__dict__,
    "accidents": context.accidents.__dict__,
    "recommendations": [recommendation.__dict__ for recommendation in recommendations],
}

st.download_button(
    label="📥 Download Report (JSON)",
    data=json.dumps(
        report,
        indent=4,
    ),
    file_name="urban_planning_report.json",
    mime="application/json",
)

st.success("Report generated successfully.")
