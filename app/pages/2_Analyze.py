"""
Analyze Page

Upload a satellite image and perform
AI-based urban analysis.
"""

from pathlib import Path

import streamlit as st

from backend.prediction.utils import PredictionPipeline

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Analyze",
    page_icon="🛰️",
    layout="wide",
)

# ==========================================================
# Header
# ==========================================================

st.title("🛰️ AI Urban Analysis")

st.write("""
Upload a satellite image of Bengaluru and select
the corresponding area and ward for analysis.
""")

st.divider()

# ==========================================================
# Sidebar Inputs
# ==========================================================

st.sidebar.header("Study Area")

area = st.sidebar.selectbox(
    "Select Area",
    [
        "Indiranagar",
        "Koramangala",
        "Whitefield",
        "Jayanagar",
        "M.G. Road",
    ],
)

ward = st.sidebar.selectbox(
    "Select Ward",
    [
        "Kempegowda Ward",
        "Jakkuru",
        "Thanisandra",
        "Vidyaranyapura",
        "Atturu",
    ],
)

uploaded_file = st.file_uploader(
    "Upload Satellite Image",
    type=["jpg", "jpeg", "png", "tif", "tiff"],
)

# ==========================================================
# Run Analysis
# ==========================================================

if uploaded_file is not None:

    upload_dir = Path("outputs/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    image_path = upload_dir / uploaded_file.name

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Image uploaded successfully.")

    if st.button("🚀 Analyze Image"):

        with st.spinner("Running AI Model..."):

            pipeline = PredictionPipeline(model_path="checkpoints/best_model.keras")

            result = pipeline.run(image_path)

        # ---------------------------------------------
        # Save everything in session state
        # ---------------------------------------------

        st.session_state["analysis"] = result
        st.session_state["area"] = area
        st.session_state["ward"] = ward

        st.success("Analysis Complete!")

# ==========================================================
# Display Results
# ==========================================================

if "analysis" in st.session_state:

    result = st.session_state["analysis"]

    st.divider()

    st.header("Prediction Results")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Original Image")

        st.image(
            result["original_image"],
            use_container_width=True,
        )

    with col2:

        st.subheader("Segmentation Overlay")

        st.image(
            result["overlay_image"],
            use_container_width=True,
        )

    st.divider()

    st.subheader("Colored Segmentation Mask")

    st.image(
        result["colored_mask"],
        use_container_width=True,
    )

    st.success("Go to the Dashboard page to view detailed statistics.")
