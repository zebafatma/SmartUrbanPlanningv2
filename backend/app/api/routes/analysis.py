"""
analysis.py

API route for satellite image analysis.
"""

from pathlib import Path
from uuid import uuid4

import cv2
from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.configs.config import BEST_MODEL_PATH
from backend.prediction.utils import PredictionPipeline

# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/api",
    tags=["Analysis"],
)


# ==========================================================
# Directories
# ==========================================================

UPLOAD_DIR = Path("backend/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# Prediction Pipeline
# ==========================================================

pipeline = PredictionPipeline(model_path=BEST_MODEL_PATH)


# ==========================================================
# Analyze Image
# ==========================================================


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
):
    """
    Analyze an uploaded satellite image.

    Returns:
        - segmentation statistics
        - original image
        - colored segmentation mask
        - overlay image
    """

    # ------------------------------------------------------
    # Validate file type
    # ------------------------------------------------------

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".tif",
        ".tiff",
    }

    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=("Unsupported image format. " "Use JPG, JPEG, PNG, TIF, or TIFF."),
        )

    # ------------------------------------------------------
    # Save uploaded image
    # ------------------------------------------------------

    file_name = f"{uuid4().hex}" f"{file_extension}"

    image_path = UPLOAD_DIR / file_name

    try:

        contents = await file.read()

        image_path.write_bytes(contents)

        # --------------------------------------------------
        # Run prediction
        # --------------------------------------------------

        result = pipeline.run(image_path)

        # --------------------------------------------------
        # Convert images to base64
        # --------------------------------------------------

        original_image = _image_to_base64(result["original_image"])

        colored_mask = _image_to_base64(result["colored_mask"])

        overlay_image = _image_to_base64(result["overlay_image"])

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return {
            "success": True,
            "statistics": result["statistics"],
            "images": {
                "original": original_image,
                "mask": colored_mask,
                "overlay": overlay_image,
            },
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Image analysis failed: {exc}",
        ) from exc

    finally:

        # --------------------------------------------------
        # Remove uploaded file
        # --------------------------------------------------

        if image_path.exists():

            image_path.unlink()


# ==========================================================
# Image → Base64
# ==========================================================


def _image_to_base64(image) -> str:
    """
    Convert an OpenCV/RGB image into a base64 data URL.
    """

    import base64

    success, encoded_image = cv2.imencode(
        ".png",
        cv2.cvtColor(
            image,
            cv2.COLOR_RGB2BGR,
        ),
    )

    if not success:

        raise ValueError("Failed to encode image.")

    encoded = base64.b64encode(encoded_image.tobytes()).decode("utf-8")

    return "data:image/png;base64," + encoded
