"""
locations.py

API routes for retrieving available mapped
Bangalore locations.
"""

from fastapi import APIRouter

from backend.recommendation.data_loader import ExternalDataLoader

# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/api/locations",
    tags=["Locations"],
)


# ==========================================================
# Data Loader
# ==========================================================

loader = ExternalDataLoader()


# ==========================================================
# Locations
# ==========================================================


@router.get("/")
def get_locations():

    mapping = loader.load_location_mapping()

    locations = (
        mapping[
            [
                "area_name",
                "ward_name",
                "mapping_type",
            ]
        ]
        .dropna(
            subset=[
                "area_name",
                "ward_name",
            ]
        )
        .to_dict(orient="records")
    )

    return {
        "success": True,
        "locations": locations,
    }
