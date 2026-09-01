"""
data_loader.py

Loads all external datasets used by the recommendation engine.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd


class ExternalDataLoader:
    """
    Loads external datasets.

    Datasets:
        - Traffic
        - Population
        - Weather
        - Accidents
        - Amenities
        - Ward Boundaries
    """

    def __init__(self):

        self.base_path = Path("data/external")

        self._traffic = None
        self._population = None
        self._weather = None
        self._accidents = None
        self._wards = None
        self._location_mapping = None

        self._amenities = {}

    # =====================================================
    # Generic CSV Loader
    # =====================================================

    @staticmethod
    def _load_csv(path: Path):

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_csv(path)

    # =====================================================
    # Generic GeoJSON Loader
    # =====================================================

    @staticmethod
    def _load_geojson(path: Path):

        if not path.exists():
            raise FileNotFoundError(path)

        return gpd.read_file(path)

    # =====================================================
    # Traffic
    # =====================================================

    def load_traffic(self):

        if self._traffic is None:

            self._traffic = self._load_csv(
                self.base_path / "traffic" / "banglore_traffic.csv"
            )

        return self._traffic

    # =====================================================
    # Population
    # =====================================================

    def load_population(self):

        if self._population is None:

            self._population = self._load_csv(
                self.base_path / "population" / "ward_population.csv"
            )

        return self._population

    # =====================================================
    # Weather
    # =====================================================

    def load_weather(self):

        if self._weather is None:

            self._weather = self._load_csv(self.base_path / "weather" / "weather.csv")

        return self._weather

    # =====================================================
    # Accidents
    # =====================================================

    def load_accidents(self):

        if self._accidents is None:

            self._accidents = self._load_csv(
                self.base_path / "accidents" / "accidents.csv"
            )

        return self._accidents

    # =====================================================
    # Ward Boundaries
    # =====================================================

    def load_wards(self):

        if self._wards is None:

            self._wards = self._load_geojson(
                self.base_path / "boundaries" / "wards.geojson"
            )

        return self._wards

    # =====================================================
    # Location Mapping
    # =====================================================

    def load_location_mapping(self):

        if self._location_mapping is None:

            self._location_mapping = self._load_csv(
                self.base_path / "mapping" / "location_mapping.csv"
            )

        return self._location_mapping

    # =====================================================
    # Amenities
    # =====================================================

    def load_amenity(self, name: str):
        """
        Example:

        load_amenity("hospitals")

        load_amenity("schools")

        load_amenity("metro")

        load_amenity("bus_stops")
        """

        if name not in self._amenities:

            self._amenities[name] = self._load_geojson(
                self.base_path / "amenities" / f"{name}.geojson"
            )

        return self._amenities[name]

    # =====================================================
    # Dataset Summary
    # =====================================================

    def summary(self):

        print()

        print("Traffic      :", len(self.load_traffic()))

        print("Population   :", len(self.load_population()))

        print("Weather      :", len(self.load_weather()))

        print("Accidents    :", len(self.load_accidents()))

        print("Wards        :", len(self.load_wards()))

        print()
