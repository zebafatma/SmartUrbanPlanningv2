"""
report.py

API route for generating an urban planning report.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.recommendation.context_builder import ContextBuilder

# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/api/report",
    tags=["Report"],
)


# ==========================================================
# Request Model
# ==========================================================


class ReportRequest(BaseModel):

    area: str

    ward: str

    segmentation_statistics: dict

    weather_date: str | None = None

    accident_year: int | None = None


# ==========================================================
# Context Builder
# ==========================================================

context_builder = ContextBuilder()


# ==========================================================
# Generate Report Data
# ==========================================================


@router.post("/")
def generate_report(
    request: ReportRequest,
):
    """
    Generate complete urban planning report data.

    The report currently returns structured JSON.
    PDF generation will be added later.
    """

    try:

        context = context_builder.build(
            segmentation_statistics=(request.segmentation_statistics),
            area_name=request.area,
            ward_name=request.ward,
            weather_date=request.weather_date,
            accident_year=request.accident_year,
        )

        report_data = ContextBuilder.to_dict(context)

        return {
            "success": True,
            "report": {
                "area": request.area,
                "ward": request.ward,
                "data": report_data,
            },
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(f"Failed to generate report: {exc}"),
        ) from exc
