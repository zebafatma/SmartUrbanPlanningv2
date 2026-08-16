"""
Recommendations Page

Displays AI-generated urban planning recommendations.
"""

import streamlit as st

from backend.recommendation.context_builder import ContextBuilder
from backend.recommendation.engine import RecommendationEngine

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Recommendations",
    page_icon="💡",
    layout="wide",
)

st.title("💡 AI Urban Planning Recommendations")

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

# ==========================================================
# Generate Recommendations
# ==========================================================

engine = RecommendationEngine()

recommendations = engine.generate(context)

st.session_state["recommendations"] = recommendations

# ==========================================================
# Summary Cards
# ==========================================================

high = sum(r.priority == "High" for r in recommendations)

medium = sum(r.priority == "Medium" for r in recommendations)

low = sum(r.priority == "Low" for r in recommendations)

col1, col2, col3 = st.columns(3)

col1.metric(
    "🔴 High Priority",
    high,
)

col2.metric(
    "🟡 Medium Priority",
    medium,
)

col3.metric(
    "🟢 Low Priority",
    low,
)

st.divider()

# ==========================================================
# Display Recommendations
# ==========================================================

st.header("Planning Suggestions")

if len(recommendations) == 0:

    st.success("No major issues detected. Current urban conditions are satisfactory.")

else:

    priority_color = {
        "High": "🔴",
        "Medium": "🟡",
        "Low": "🟢",
    }

    for recommendation in recommendations:

        with st.expander(
            f"{priority_color[recommendation.priority]} " f"{recommendation.title}",
            expanded=True,
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**Priority:** {recommendation.priority}")

                st.write(f"**Category:** {recommendation.category}")

            with col2:

                st.write("**Recommendation**")

                st.write(recommendation.description)

st.divider()

# ==========================================================
# Overall Assessment
# ==========================================================

st.header("Overall Assessment")

if high == 0:

    st.success("""
        The selected area appears to have balanced urban characteristics.
        Only routine improvements are recommended.
        """)

elif high <= 2:

    st.warning("""
        Moderate urban planning improvements are recommended.
        Priority should be given to high-impact issues.
        """)

else:

    st.error("""
        Multiple critical issues have been identified.
        Immediate planning interventions are recommended.
        """)
