"""
report.py

Urban planning recommendation engine.

Uses the consolidated UrbanContext to generate
rule-based planning recommendations.
"""

from dataclasses import dataclass
from typing import List

# ==========================================================
# Recommendation
# ==========================================================


@dataclass
class Recommendation:

    title: str

    description: str

    category: str

    priority: str

    impact: str

    confidence: float


# ==========================================================
# Recommendation Engine
# ==========================================================


class RecommendationEngine:
    """
    Generates urban planning recommendations from
    the consolidated UrbanContext.
    """

    def generate(self, context) -> List[Recommendation]:

        recommendations = []

        # --------------------------------------------------
        # Satellite / Land Cover
        # --------------------------------------------------

        self._land_cover_recommendations(
            context,
            recommendations,
        )

        # --------------------------------------------------
        # Traffic
        # --------------------------------------------------

        self._traffic_recommendations(
            context,
            recommendations,
        )

        # --------------------------------------------------
        # Population
        # --------------------------------------------------

        self._population_recommendations(
            context,
            recommendations,
        )

        # --------------------------------------------------
        # Road Safety
        # --------------------------------------------------

        self._accident_recommendations(
            context,
            recommendations,
        )

        # --------------------------------------------------
        # Weather / Climate
        # --------------------------------------------------

        self._weather_recommendations(
            context,
            recommendations,
        )

        # --------------------------------------------------
        # Amenities
        # --------------------------------------------------

        self._amenity_recommendations(
            context,
            recommendations,
        )

        # --------------------------------------------------
        # Sort
        # --------------------------------------------------

        priority_order = {
            "Critical": 0,
            "High": 1,
            "Medium": 2,
            "Low": 3,
        }

        recommendations.sort(
            key=lambda item: priority_order.get(
                item.priority,
                4,
            )
        )

        return recommendations

    # ======================================================
    # Land Cover
    # ======================================================

    @staticmethod
    def _land_cover_recommendations(
        context,
        recommendations,
    ):

        segmentation = context.segmentation

        # --------------------------------------------------
        # Low vegetation
        # --------------------------------------------------

        if segmentation.vegetation_percentage < 20:

            recommendations.append(
                Recommendation(
                    title="Increase green coverage",
                    description=(
                        "Vegetation coverage is relatively low. "
                        "Consider increasing urban green spaces, "
                        "tree cover, and landscaped areas."
                    ),
                    category="Environment",
                    priority="High",
                    impact="High",
                    confidence=0.85,
                )
            )

        # --------------------------------------------------
        # High building coverage
        # --------------------------------------------------

        if segmentation.building_percentage > 40:

            recommendations.append(
                Recommendation(
                    title="Improve open-space availability",
                    description=(
                        "Building coverage occupies a large "
                        "portion of the analyzed area. "
                        "Preserving or introducing accessible "
                        "open spaces can improve urban livability."
                    ),
                    category="Land Use",
                    priority="High",
                    impact="High",
                    confidence=0.82,
                )
            )

        # --------------------------------------------------
        # High vegetation
        # --------------------------------------------------

        if segmentation.vegetation_percentage >= 40:

            recommendations.append(
                Recommendation(
                    title="Protect existing green areas",
                    description=(
                        "The analyzed area has substantial "
                        "vegetation coverage. Future development "
                        "should prioritize preserving existing "
                        "green areas."
                    ),
                    category="Environment",
                    priority="Medium",
                    impact="High",
                    confidence=0.80,
                )
            )

    # ======================================================
    # Traffic
    # ======================================================

    @staticmethod
    def _traffic_recommendations(
        context,
        recommendations,
    ):

        traffic = context.traffic

        # --------------------------------------------------
        # Severe congestion
        # --------------------------------------------------

        if traffic.traffic_category == "Severe":

            recommendations.append(
                Recommendation(
                    title="Prioritize congestion reduction",
                    description=(
                        "Traffic conditions are classified as "
                        "severe. Consider improving traffic flow, "
                        "public transport availability, and "
                        "intersection management."
                    ),
                    category="Mobility",
                    priority="Critical",
                    impact="High",
                    confidence=0.92,
                )
            )

        # --------------------------------------------------
        # High congestion
        # --------------------------------------------------

        elif traffic.traffic_category == "High":

            recommendations.append(
                Recommendation(
                    title="Improve urban mobility",
                    description=(
                        "Traffic conditions are classified as "
                        "high. Improvements to public transport "
                        "and traffic management may help reduce "
                        "congestion."
                    ),
                    category="Mobility",
                    priority="High",
                    impact="High",
                    confidence=0.88,
                )
            )

        # --------------------------------------------------
        # Low public transport usage
        # --------------------------------------------------

        if traffic.public_transport_usage < 20:

            recommendations.append(
                Recommendation(
                    title="Encourage public transport usage",
                    description=(
                        "Public transport usage is relatively low. "
                        "Improving accessibility and connectivity "
                        "could encourage a shift away from private "
                        "vehicles."
                    ),
                    category="Mobility",
                    priority="Medium",
                    impact="Medium",
                    confidence=0.76,
                )
            )

    # ======================================================
    # Population
    # ======================================================

    @staticmethod
    def _population_recommendations(
        context,
        recommendations,
    ):

        population = context.population

        # --------------------------------------------------
        # Very high density
        # --------------------------------------------------

        if population.population_category == "Very High":

            recommendations.append(
                Recommendation(
                    title="Strengthen high-density infrastructure",
                    description=(
                        "Population density is very high. "
                        "Infrastructure capacity, public transport, "
                        "and essential services should be planned "
                        "to support the concentrated population."
                    ),
                    category="Infrastructure",
                    priority="High",
                    impact="High",
                    confidence=0.88,
                )
            )

        # --------------------------------------------------
        # High density
        # --------------------------------------------------

        elif population.population_category == "High":

            recommendations.append(
                Recommendation(
                    title="Plan infrastructure for population pressure",
                    description=(
                        "The area has high population density. "
                        "Future infrastructure planning should "
                        "account for increasing demand on public "
                        "services and mobility."
                    ),
                    category="Infrastructure",
                    priority="Medium",
                    impact="High",
                    confidence=0.82,
                )
            )

        # --------------------------------------------------
        # Low infrastructure score
        # --------------------------------------------------

        if population.infrastructure_score < 30:

            recommendations.append(
                Recommendation(
                    title="Improve basic infrastructure",
                    description=(
                        "The calculated infrastructure score is "
                        "low. Priority should be given to improving "
                        "essential infrastructure and public services."
                    ),
                    category="Infrastructure",
                    priority="High",
                    impact="High",
                    confidence=0.84,
                )
            )

    # ======================================================
    # Accidents
    # ======================================================

    @staticmethod
    def _accident_recommendations(
        context,
        recommendations,
    ):

        accidents = context.accidents

        # --------------------------------------------------
        # Critical safety
        # --------------------------------------------------

        if accidents.safety_category == "Critical":

            recommendations.append(
                Recommendation(
                    title="Prioritize road safety",
                    description=(
                        "The accident severity index indicates "
                        "critical road-safety conditions. "
                        "Safety interventions should be prioritized "
                        "for high-risk road environments."
                    ),
                    category="Road Safety",
                    priority="Critical",
                    impact="High",
                    confidence=0.93,
                )
            )

        # --------------------------------------------------
        # Risky
        # --------------------------------------------------

        elif accidents.safety_category == "Risky":

            recommendations.append(
                Recommendation(
                    title="Strengthen road safety measures",
                    description=(
                        "The accident severity index indicates "
                        "elevated road-safety risk. Consider "
                        "additional safety measures and traffic "
                        "management interventions."
                    ),
                    category="Road Safety",
                    priority="High",
                    impact="High",
                    confidence=0.87,
                )
            )

        # --------------------------------------------------
        # Increasing accidents
        # --------------------------------------------------

        if accidents.yearly_change > 10:

            recommendations.append(
                Recommendation(
                    title="Investigate rising accident trends",
                    description=(
                        "The number of recorded accidents has "
                        "increased significantly compared with "
                        "the previous year. Further investigation "
                        "of accident-prone locations is recommended."
                    ),
                    category="Road Safety",
                    priority="High",
                    impact="High",
                    confidence=0.89,
                )
            )

    # ======================================================
    # Weather
    # ======================================================

    @staticmethod
    def _weather_recommendations(
        context,
        recommendations,
    ):

        weather = context.weather

        # --------------------------------------------------
        # Extreme heat
        # --------------------------------------------------

        if weather.heat_risk == "Extreme":

            recommendations.append(
                Recommendation(
                    title="Mitigate extreme heat exposure",
                    description=(
                        "Current weather conditions indicate "
                        "extreme heat risk. Increasing shade, "
                        "vegetation, and heat-resilient public "
                        "spaces can improve outdoor comfort."
                    ),
                    category="Climate",
                    priority="High",
                    impact="High",
                    confidence=0.91,
                )
            )

        # --------------------------------------------------
        # High heat
        # --------------------------------------------------

        elif weather.heat_risk == "High":

            recommendations.append(
                Recommendation(
                    title="Improve heat resilience",
                    description=(
                        "High heat risk has been detected. "
                        "Urban greening and shaded public spaces "
                        "can help reduce heat exposure."
                    ),
                    category="Climate",
                    priority="Medium",
                    impact="Medium",
                    confidence=0.84,
                )
            )

        # --------------------------------------------------
        # Heavy rainfall
        # --------------------------------------------------

        if weather.weather_category == "Heavy Rain":

            recommendations.append(
                Recommendation(
                    title="Prepare for heavy rainfall",
                    description=(
                        "Heavy rainfall conditions have been "
                        "detected. Drainage capacity and flood "
                        "preparedness should be considered in "
                        "urban planning."
                    ),
                    category="Climate",
                    priority="High",
                    impact="High",
                    confidence=0.86,
                )
            )

    # ======================================================
    # Amenities
    # ======================================================

    @staticmethod
    def _amenity_recommendations(
        context,
        recommendations,
    ):

        amenities = context.amenities

        # --------------------------------------------------
        # Hospitals
        # --------------------------------------------------

        hospitals = amenities.get("Hospitals")

        if hospitals and hospitals.total_features == 0:

            recommendations.append(
                Recommendation(
                    title="Improve healthcare accessibility",
                    description=(
                        "No hospital features were detected "
                        "in the available hospital dataset. "
                        "Healthcare accessibility should be "
                        "reviewed for the selected area."
                    ),
                    category="Public Services",
                    priority="High",
                    impact="High",
                    confidence=0.78,
                )
            )

        # --------------------------------------------------
        # Schools
        # --------------------------------------------------

        schools = amenities.get("Schools")

        if schools and schools.total_features == 0:

            recommendations.append(
                Recommendation(
                    title="Review educational access",
                    description=(
                        "No school features were detected "
                        "in the available dataset. Educational "
                        "accessibility should be reviewed."
                    ),
                    category="Public Services",
                    priority="Medium",
                    impact="Medium",
                    confidence=0.75,
                )
            )

        # --------------------------------------------------
        # Bus Stops
        # --------------------------------------------------

        bus_stops = amenities.get("Bus Stops")

        if bus_stops and bus_stops.total_features == 0:

            recommendations.append(
                Recommendation(
                    title="Review public transport coverage",
                    description=(
                        "No bus-stop features were detected "
                        "in the available dataset. Public "
                        "transport accessibility should be reviewed."
                    ),
                    category="Mobility",
                    priority="High",
                    impact="High",
                    confidence=0.79,
                )
            )

    # ======================================================
    # Dictionary
    # ======================================================

    @staticmethod
    def to_dict(
        recommendation: Recommendation,
    ) -> dict:

        return recommendation.__dict__
