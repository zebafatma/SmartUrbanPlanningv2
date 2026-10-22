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

# Analyzers are created on first use (not at import time), so the API can
# start and serve /api/analyze even if data/external is not present yet.

from functools import lru_cache


@lru_cache(maxsize=1)
def _analyzers():
    return {
        "traffic": TrafficAnalyzer(),
        "population": PopulationAnalyzer(),
        "weather": WeatherAnalyzer(),
        "accidents": AccidentAnalyzer(),
        "amenities": AmenityAnalyzer(),
    }

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
            "locations": _analyzers()["population"].get_locations(),
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
        traffic = _analyzers()["traffic"].analyze(area)
        print("traffic")
        # --------------------------------------------------
        # Population
        # --------------------------------------------------
        print("popluation s")
        population = _analyzers()["population"].analyze(ward)
        print("population e")

        # --------------------------------------------------
        # Weather
        # --------------------------------------------------
        print("weather s")
        weather = _analyzers()["weather"].latest()
        print("weather e")
        # --------------------------------------------------
        # Accidents
        # --------------------------------------------------
        print("accisdents s")
        accidents = _analyzers()["accidents"].latest()
        print("accidents e")
        # --------------------------------------------------
        # Amenities
        # --------------------------------------------------
        print("amneties s")

        print("hospitals s")
        hospitals = _analyzers()["amenities"].analyze("hospitals")
        print("hospitals e")

        print("schools s")
        schools = _analyzers()["amenities"].analyze("schools")
        print("schools e")

        print("bus stops s")
        bus_stops = _analyzers()["amenities"].analyze("bus_stops")
        print("bus stops e")

        print("metro s")
        metro = _analyzers()["amenities"].analyze("metro")
        print("metro e")

        print("parks s")
        parks = _analyzers()["amenities"].analyze("parks")
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
