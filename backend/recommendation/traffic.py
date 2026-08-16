"""
traffic.py

Traffic analysis module.

Analyzes traffic conditions and produces
standardized traffic information for the
recommendation engine.
"""

from dataclasses import dataclass

import pandas as pd

from backend.recommendation.data_loader import ExternalDataLoader

# ==========================================================
# Traffic Features
# ==========================================================


@dataclass
class TrafficFeatures:

    area: str

    road: str

    congestion_level: float

    average_speed: float

    traffic_volume: int

    travel_time_index: float

    road_capacity: float

    incidents: int

    public_transport_usage: float

    environmental_impact: float

    parking_usage: float

    pedestrian_count: int

    weather: str

    roadwork: str

    traffic_score: float

    traffic_category: str


# ==========================================================
# Traffic Analyzer
# ==========================================================


class TrafficAnalyzer:

    def __init__(self):

        self.loader = ExternalDataLoader()

        self.df = self.loader.load_traffic()

    # ======================================================
    # Area Lookup
    # ======================================================

    def get_area_data(
        self,
        area_name: str,
    ) -> pd.DataFrame:

        area = self.df[self.df["Area Name"].str.lower() == area_name.lower()]

        if area.empty:

            raise ValueError(f"No traffic data found for '{area_name}'.")

        return area

    # ======================================================
    # Traffic Score
    # ======================================================

    def calculate_score(
        self,
        row,
    ) -> float:

        score = (
            row["Congestion Level"] * 0.30
            + row["Road Capacity Utilization"] * 0.20
            + row["Traffic Volume"] / 1000 * 0.10
            + row["Incident Reports"] * 5
            + row["Environmental Impact"] * 0.10
            + (100 - row["Average Speed"]) * 0.20
            + row["Travel Time Index"] * 10 * 0.10
        )

        return round(score, 2)

    # ======================================================
    # Category
    # ======================================================

    @staticmethod
    def classify(score):

        if score < 30:

            return "Low"

        elif score < 50:

            return "Moderate"

        elif score < 70:

            return "High"

        return "Severe"

    # ======================================================
    # Analyze
    # ======================================================

    def analyze(
        self,
        area_name,
    ):

        area = self.get_area_data(
            area_name,
        )

        row = area.iloc[0]

        score = self.calculate_score(
            row,
        )

        category = self.classify(
            score,
        )

        return TrafficFeatures(
            area=row["Area Name"],
            road=row["Road/Intersection Name"],
            congestion_level=row["Congestion Level"],
            average_speed=row["Average Speed"],
            traffic_volume=row["Traffic Volume"],
            travel_time_index=row["Travel Time Index"],
            road_capacity=row["Road Capacity Utilization"],
            incidents=row["Incident Reports"],
            public_transport_usage=row["Public Transport Usage"],
            environmental_impact=row["Environmental Impact"],
            parking_usage=row["Parking Usage"],
            pedestrian_count=row["Pedestrian and Cyclist Count"],
            weather=row["Weather Conditions"],
            roadwork=row["Roadwork and Construction Activity"],
            traffic_score=score,
            traffic_category=category,
        )

    # ======================================================
    # Dictionary Output
    # ======================================================

    @staticmethod
    def to_dict(
        traffic: TrafficFeatures,
    ):

        return traffic.__dict__
