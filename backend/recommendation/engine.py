"""
engine.py

Urban Planning Recommendation Engine.
"""

from dataclasses import dataclass
from typing import List

from backend.recommendation.context_builder import UrbanContext

# ==========================================================
# Recommendation
# ==========================================================


@dataclass
class Recommendation:

    priority: str

    category: str

    title: str

    description: str


# ==========================================================
# Recommendation Engine
# ==========================================================


class RecommendationEngine:

    def __init__(self):

        self.recommendations = []

    # ======================================================
    # Helpers
    # ======================================================

    def add(
        self,
        priority,
        category,
        title,
        description,
    ):

        self.recommendations.append(
            Recommendation(
                priority,
                category,
                title,
                description,
            )
        )

    # ======================================================
    # Road Rules
    # ======================================================

    def road_rules(
        self,
        context: UrbanContext,
    ):

        if context.segmentation.road_percentage < 15:

            self.add(
                "High",
                "Transportation",
                "Increase Road Connectivity",
                "Detected road coverage is very low. Consider widening existing roads or constructing new road links.",
            )

        if context.traffic.traffic_category in [
            "High",
            "Severe",
        ]:

            self.add(
                "High",
                "Traffic",
                "Traffic Congestion",
                "Traffic congestion is high. Intelligent traffic management or road expansion is recommended.",
            )

    # ======================================================
    # Vegetation Rules
    # ======================================================

    def vegetation_rules(
        self,
        context,
    ):

        if context.segmentation.vegetation_percentage < 20:

            self.add(
                "High",
                "Environment",
                "Increase Green Spaces",
                "Vegetation cover is low. Develop parks and roadside plantations.",
            )

    # ======================================================
    # Water Rules
    # ======================================================

    def water_rules(
        self,
        context,
    ):

        if context.segmentation.water_percentage < 3:

            self.add(
                "Medium",
                "Water",
                "Improve Water Conservation",
                "Water body coverage is limited. Rainwater harvesting and lake restoration are recommended.",
            )

    # ======================================================
    # Population Rules
    # ======================================================

    def population_rules(
        self,
        context,
    ):

        if context.population.population_category == "Very High":

            self.add(
                "High",
                "Urban Planning",
                "High Population Density",
                "High population density indicates the need for better infrastructure planning.",
            )

    # ======================================================
    # Weather Rules
    # ======================================================

    def weather_rules(
        self,
        context,
    ):

        if context.weather.heat_risk in [
            "High",
            "Extreme",
        ]:

            self.add(
                "Medium",
                "Climate",
                "Heat Island Mitigation",
                "Increase tree cover and reflective surfaces to reduce urban heat.",
            )

    # ======================================================
    # Accident Rules
    # ======================================================

    def accident_rules(
        self,
        context,
    ):

        if context.accidents.safety_category in [
            "Risky",
            "Critical",
        ]:

            self.add(
                "High",
                "Road Safety",
                "Improve Road Safety",
                "Frequent accidents indicate the need for better road design and enforcement.",
            )

    # ======================================================
    # Amenity Rules
    # ======================================================

    def amenity_rules(
        self,
        context,
    ):

        hospitals = context.amenities["Hospitals"]

        schools = context.amenities["Schools"]

        parks = context.amenities["Parks"]

        if hospitals.total_features < 30:

            self.add(
                "Medium",
                "Healthcare",
                "Increase Healthcare Facilities",
                "Few hospitals detected in the study region.",
            )

        if schools.total_features < 30:

            self.add(
                "Medium",
                "Education",
                "Increase Educational Infrastructure",
                "School availability is limited.",
            )

        if parks.total_features < 20:

            self.add(
                "Low",
                "Recreation",
                "Develop Urban Parks",
                "Increase public green recreational spaces.",
            )

    # ======================================================
    # Generate
    # ======================================================

    def generate(
        self,
        context: UrbanContext,
    ):

        self.recommendations = []

        self.road_rules(context)

        self.vegetation_rules(context)

        self.water_rules(context)

        self.population_rules(context)

        self.weather_rules(context)

        self.accident_rules(context)

        self.amenity_rules(context)

        return self.recommendations

    # ======================================================
    # Dictionary
    # ======================================================

    @staticmethod
    def to_dict(
        recommendations,
    ):

        return [recommendation.__dict__ for recommendation in recommendations]
