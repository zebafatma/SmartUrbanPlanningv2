"""
amenities.py

Generic GeoJSON amenity analyzer.

Works with:

- hospitals
- schools
- metro
- bus stops
- parks
- roads
- water bodies
"""

from dataclasses import dataclass

import geopandas as gpd

from backend.recommendation.data_loader import ExternalDataLoader

# ==========================================================
# Amenity Features
# ==========================================================


@dataclass
class AmenityFeatures:

    amenity_name: str

    total_features: int

    geometry_type: str

    bounds: tuple

    centroid_latitude: float

    centroid_longitude: float


# ==========================================================
# Amenity Analyzer
# ==========================================================


class AmenityAnalyzer:

    def __init__(self):

        self.loader = ExternalDataLoader()

    # ======================================================
    # Analyze
    # ======================================================

    def analyze(
        self,
        amenity_name: str,
    ) -> AmenityFeatures:

        gdf = self.loader.load_amenity(
            amenity_name
        )

        if gdf.empty:
            raise ValueError(
                f"{amenity_name} dataset is empty."
            )

        geometry_type = (
            gdf.geometry.iloc[0].geom_type
        )

        bounds = tuple(
            gdf.total_bounds
        )

        # Use bounding-box center instead of
        # expensive unary_union.
        centroid_longitude = (
            bounds[0] + bounds[2]
        ) / 2

        centroid_latitude = (
            bounds[1] + bounds[3]
        ) / 2

        return AmenityFeatures(
            amenity_name=amenity_name,
            total_features=len(gdf),
            geometry_type=geometry_type,
            bounds=bounds,
            centroid_latitude=centroid_latitude,
            centroid_longitude=centroid_longitude,
        )

    # ======================================================
    # Count
    # ======================================================

    def count(
        self,
        amenity_name,
    ):

        gdf = self.loader.load_amenity(amenity_name)

        return len(gdf)

    # ======================================================
    # Load GeoDataFrame
    # ======================================================

    def dataframe(
        self,
        amenity_name,
    ) -> gpd.GeoDataFrame:

        return self.loader.load_amenity(amenity_name)

    # ======================================================
    # Dictionary
    # ======================================================

    @staticmethod
    def to_dict(
        feature,
    ):

        return feature.__dict__
