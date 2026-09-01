"""
urban_data.py

API routes for retrieving urban data.

Provides:
- Traffic information
- Population information
- Weather information
- Accident information
- Amenity information
"""

import numpy as np
from fastapi import APIRouter, HTTPException

from backend.recommendation.accidents import AccidentAnalyzer
from backend.recommendation.amenities import AmenityAnalyzer
from backend.recommendation.population import PopulationAnalyzer
from backend.recommendation.traffic import TrafficAnalyzer
from backend.recommendation.weather import WeatherAnalyzer

# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/api/urban-data",
    tags=["Urban Data"],
)


# ==========================================================
# Analyzers
# ==========================================================

traffic_analyzer = TrafficAnalyzer()

population_analyzer = PopulationAnalyzer()

weather_analyzer = WeatherAnalyzer()

accident_analyzer = AccidentAnalyzer()

amenity_analyzer = AmenityAnalyzer()

# ==========================================================
# Available Locations
# ==========================================================


@router.get("/locations")
def get_locations():
    """
    Retrieve available Bangalore areas/wards.
    """

    try:

        return {
            "success": True,
            "locations": population_analyzer.get_locations(),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve locations: {exc}",
        ) from exc


# ==========================================================
# Urban Data
# ==========================================================


@router.get("/")
def get_urban_data(
    area: str,
    ward: str,
):
    """
    Retrieve urban information for the selected
    area and ward.
    """

    try:

        # --------------------------------------------------
        # Traffic
        # --------------------------------------------------
        print("Traffic")
        traffic = traffic_analyzer.analyze(area)
        print("traffic")
        # --------------------------------------------------
        # Population
        # --------------------------------------------------
        print("popluation s")
        population = population_analyzer.analyze(ward)
        print("population e")

        # --------------------------------------------------
        # Weather
        # --------------------------------------------------
        print("weather s")
        weather = weather_analyzer.latest()
        print("weather e")
        # --------------------------------------------------
        # Accidents
        # --------------------------------------------------
        print("accisdents s")
        accidents = accident_analyzer.latest()
        print("accidents e")
        # --------------------------------------------------
        # Amenities
        # --------------------------------------------------
        print("amneties s")

        print("hospitals s")
        hospitals = amenity_analyzer.analyze("hospitals")
        print("hospitals e")

        print("schools s")
        schools = amenity_analyzer.analyze("schools")
        print("schools e")

        print("bus stops s")
        bus_stops = amenity_analyzer.analyze("bus_stops")
        print("bus stops e")

        print("metro s")
        metro = amenity_analyzer.analyze("metro")
        print("metro e")

        print("parks s")
        parks = amenity_analyzer.analyze("parks")
        print("parks e")

        amenities = {
            "Hospitals": hospitals,
            "Schools": schools,
            "Bus Stops": bus_stops,
            "Metro": metro,
            "Parks": parks,
        }
        print("amneties e")
        return {
            "success": True,
            "area": area,
            "ward": ward,
            "traffic": _serialize(traffic),
            "population": _serialize(population),
            "weather": _serialize(weather),
            "accidents": _serialize(accidents),
            "amenities": _serialize(amenities),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(f"Failed to retrieve urban data: {exc}"),
        ) from exc


# ==========================================================
# Serialization
# ==========================================================


def _serialize(value):

    if value is None:
        return None

    # ------------------------------------------------------
    # NumPy scalar values
    # ------------------------------------------------------

    if isinstance(value, np.generic):
        return value.item()

    # ------------------------------------------------------
    # NumPy arrays
    # ------------------------------------------------------

    if isinstance(value, np.ndarray):
        return value.tolist()

    # ------------------------------------------------------
    # Dictionary
    # ------------------------------------------------------

    if isinstance(value, dict):

        return {key: _serialize(item) for key, item in value.items()}

    # ------------------------------------------------------
    # List
    # ------------------------------------------------------

    if isinstance(value, list):

        return [_serialize(item) for item in value]

    # ------------------------------------------------------
    # Tuple
    # ------------------------------------------------------

    if isinstance(value, tuple):

        return [_serialize(item) for item in value]

    # ------------------------------------------------------
    # Dataclass / custom object
    # ------------------------------------------------------

    if hasattr(value, "__dict__"):

        return {
            key: _serialize(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }

    # ------------------------------------------------------
    # Normal Python value
    # ------------------------------------------------------

    return value
