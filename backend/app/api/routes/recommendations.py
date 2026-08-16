"""
recommendations.py

API routes for generating urban planning recommendations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.recommendation.context_builder import ContextBuilder
from backend.recommendation.report import RecommendationEngine


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)


# ==========================================================
# Request Model
# ==========================================================

class RecommendationRequest(BaseModel):
    area: str
    ward: str
    segmentation_statistics: dict


# ==========================================================
# Context Builder
# ==========================================================

context_builder = ContextBuilder()
recommendation_engine = RecommendationEngine()

# ==========================================================
# Generate Recommendations
# ==========================================================

@router.post("/")
def get_recommendations(
    request: RecommendationRequest,
):
    try:

        print("========== RECOMMENDATIONS START ==========")

        print("1. Request received")
        print("Area:", request.area)
        print("Ward:", request.ward)
        print("Segmentation:", request.segmentation_statistics)

        print("2. Building context")

        context = context_builder.build(
            segmentation_statistics=request.segmentation_statistics,
            area_name=request.area,
            ward_name=request.ward,
        )

        print("3. Context built")

        recommendations = recommendation_engine.generate(
            context
        )

        print("4. Recommendations generated")
        print("Recommendations:", recommendations)

        result = {
            "success": True,
            "area": request.area,
            "ward": request.ward,
            "recommendations": _serialize(
                recommendations
            ),
        }

        print("5. Response ready")
        print("========== RECOMMENDATIONS END ==========")

        return result

    except Exception as exc:

        print("!!! RECOMMENDATION ERROR !!!")
        print(repr(exc))

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {exc}",
        ) from exc

# ==========================================================
# Serialization
# ==========================================================

def _serialize(value):

    if value is None:
        return None

    if isinstance(value, dict):

        return {
            key: _serialize(item)
            for key, item in value.items()
        }

    if isinstance(value, list):

        return [
            _serialize(item)
            for item in value
        ]

    if hasattr(value, "__dict__"):

        return {
            key: _serialize(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }

    return value