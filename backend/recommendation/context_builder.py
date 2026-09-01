"""
context_builder.py

Builds a unified UrbanContext object by combining:

- Segmentation Features
- Traffic Features
- Population Features
- Weather Features
- Accident Features
- Amenity Features
"""

from dataclasses import dataclass
from typing import Dict

from backend.recommendation.accidents import AccidentAnalyzer, AccidentFeatures
from backend.recommendation.amenities import AmenityAnalyzer
from backend.recommendation.feature_extractor import FeatureExtractor, UrbanFeatures
from backend.recommendation.population import PopulationAnalyzer, PopulationFeatures
from backend.recommendation.traffic import TrafficAnalyzer, TrafficFeatures
from backend.recommendation.weather import WeatherAnalyzer, WeatherFeatures

# ==========================================================
# Urban Context
# ==========================================================


@dataclass
class UrbanContext:

    segmentation: UrbanFeatures

    traffic: TrafficFeatures

    population: PopulationFeatures

    weather: WeatherFeatures

    accidents: AccidentFeatures

    amenities: Dict


# ==========================================================
# Context Builder
# ==========================================================


class ContextBuilder:

    def __init__(self):

        self.feature_extractor = FeatureExtractor()

        self.traffic = TrafficAnalyzer()

        self.population = PopulationAnalyzer()

        self.weather = WeatherAnalyzer()

        self.accidents = AccidentAnalyzer()

        self.amenities = AmenityAnalyzer()

    # ======================================================
    # Build Context
    # ======================================================

    def build(
        self,
        segmentation_statistics,
        area_name,
        ward_name,
        weather_date=None,
        accident_year=None,
    ) -> UrbanContext:
        print("CONTEXT: segmentation start")

        # -----------------------------------------
        # Segmentation
        # -----------------------------------------

        segmentation = self.feature_extractor.extract(segmentation_statistics)
        print("CONTEXT: segmentation done")
        # -----------------------------------------
        # Traffic
        # -----------------------------------------
        print("CONTEXT: traffic start")
        traffic = self.traffic.analyze(area_name)
        print("CONTEXT: traffic done")

        print("CONTEXT: population start")
        # -----------------------------------------
        # Population
        # -----------------------------------------

        population = self.population.analyze(ward_name)
        print("CONTEXT: population done")

        print("CONTEXT: weather start")
        # -----------------------------------------
        # Weather
        # -----------------------------------------

        if weather_date is None:

            weather = self.weather.latest()

        else:

            weather = self.weather.by_date(weather_date)

        # -----------------------------------------
        # Accidents
        # -----------------------------------------
        print("CONTEXT: weather done")

        print("CONTEXT: accidents start")
        if accident_year is None:

            accidents = self.accidents.latest()

        else:

            accidents = self.accidents.by_year(accident_year)

        # -----------------------------------------
        # Amenities
        # -----------------------------------------
        print("CONTEXT: accidents done")

        print("CONTEXT: amenities start")
        print("HOSPITALS start")
        hospitals = self.amenities.analyze("hospitals")
        print("HOSPITALS done")

        print("SCHOOLS start")
        schools = self.amenities.analyze("schools")
        print("SCHOOLS done")

        print("BUS STOPS start")
        bus_stops = self.amenities.analyze("bus_stops")
        print("BUS STOPS done")

        print("METRO start")
        metro = self.amenities.analyze("metro")
        print("METRO done")

        print("PARKS start")
        parks = self.amenities.analyze("parks")
        print("PARKS done")

        amenities = {
            "Hospitals": hospitals,
            "Schools": schools,
            "Bus Stops": bus_stops,
            "Metro": metro,
            "Parks": parks,
        }
        print("CONTEXT: amenities done")

        print("CONTEXT: building UrbanContext")
        return UrbanContext(
            segmentation=segmentation,
            traffic=traffic,
            population=population,
            weather=weather,
            accidents=accidents,
            amenities=amenities,
        )

    # ======================================================
    # Dictionary
    # ======================================================

    @staticmethod
    def to_dict(
        context,
    ):

        return {
            "segmentation": context.segmentation.__dict__,
            "traffic": context.traffic.__dict__,
            "population": context.population.__dict__,
            "weather": context.weather.__dict__,
            "accidents": context.accidents.__dict__,
            "amenities": {
                key: value.__dict__ for key, value in context.amenities.items()
            },
        }
