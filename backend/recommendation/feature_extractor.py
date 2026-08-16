"""
feature_extractor.py

Converts segmentation statistics into
features for the recommendation engine.
"""

from dataclasses import dataclass

# ==========================================================
# Urban Features
# ==========================================================


@dataclass
class UrbanFeatures:

    road_percentage: float

    building_percentage: float

    vegetation_percentage: float

    water_percentage: float

    background_percentage: float

    total_pixels: int


# ==========================================================
# Feature Extractor
# ==========================================================


class FeatureExtractor:
    """
    Converts prediction statistics into
    UrbanFeatures.
    """

    def extract(
        self,
        statistics: dict,
    ) -> UrbanFeatures:

        percentages = statistics["percentages"]

        pixels = statistics["pixel_counts"]

        return UrbanFeatures(
            road_percentage=percentages.get(
                "Road",
                0.0,
            ),
            building_percentage=percentages.get(
                "Building",
                0.0,
            ),
            vegetation_percentage=percentages.get(
                "Vegetation",
                0.0,
            ),
            water_percentage=percentages.get(
                "Water",
                0.0,
            ),
            background_percentage=percentages.get(
                "Background",
                0.0,
            ),
            total_pixels=pixels.get(
                "Total Pixels",
                0,
            ),
        )

    # ======================================================
    # Dictionary Output
    # ======================================================

    def to_dict(
        self,
        features: UrbanFeatures,
    ) -> dict:

        return {
            "road_percentage": features.road_percentage,
            "building_percentage": features.building_percentage,
            "vegetation_percentage": features.vegetation_percentage,
            "water_percentage": features.water_percentage,
            "background_percentage": features.background_percentage,
            "total_pixels": features.total_pixels,
        }
