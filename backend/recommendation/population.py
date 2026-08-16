"""
population.py

Population and infrastructure analysis module.
"""

from dataclasses import dataclass

import pandas as pd

from backend.recommendation.data_loader import ExternalDataLoader

# ==========================================================
# Population Features
# ==========================================================


@dataclass
class PopulationFeatures:

    ward_number: int

    ward_name: str

    zone: str

    population: int

    area_sq_km: float

    population_density: float

    households: int

    road_length: float

    parks: int

    lakes: int

    bus_stops: int

    government_schools: int

    police_stations: int

    fire_stations: int

    streetlights: int

    growth_rate: float

    infrastructure_score: float

    population_category: str


# ==========================================================
# Population Analyzer
# ==========================================================


class PopulationAnalyzer:

    def __init__(self):

        self.loader = ExternalDataLoader()

        self.df = self.loader.load_population()

    # ======================================================
    # Cleaning Helpers
    # ======================================================

    @staticmethod
    def _to_float(value):

        if pd.isna(value):
            return 0.0

        return float(str(value).replace(",", "").replace("%", ""))

    # ======================================================
    # Ward Lookup
    # ======================================================

    def get_ward_data(
        self,
        ward_name,
    ):

        ward = self.df[self.df["Ward Name"].str.lower() == ward_name.lower()]

        if ward.empty:

            raise ValueError(f"Ward '{ward_name}' not found.")

        return ward.iloc[0]

    # ======================================================
    # Infrastructure Score
    # ======================================================

    def infrastructure_score(
        self,
        row,
    ):

        road_length = self._to_float(row["Road Length (kms)"])

        bus_stops = self._to_float(row["Bus Stops #"])

        schools = self._to_float(row["Govt Schools #"])

        police = self._to_float(row["Police Stations #"])

        fire = self._to_float(row["Fire stations #"])

        streetlights = self._to_float(row["Streetlights #"])

        parks = self._to_float(row["Parks #"])

        lakes = self._to_float(row["Lakes #"])

        score = (
            road_length * 0.20
            + bus_stops * 0.15
            + schools * 0.10
            + police * 0.10
            + fire * 0.10
            + (streetlights / 100) * 0.20
            + parks * 0.10
            + lakes * 0.05
        )

        return round(score, 2)

    # ======================================================
    # Population Category
    # ======================================================

    @staticmethod
    def classify_population(
        density,
    ):

        if density < 3000:

            return "Low"

        elif density < 7000:

            return "Moderate"

        elif density < 12000:

            return "High"

        return "Very High"

    # ======================================================
    # Analyze
    # ======================================================

    def analyze(
        self,
        ward_name,
    ):

        row = self.get_ward_data(
            ward_name,
        )

        density = self._to_float(row["Population density 2011 (persons / sq km)"])

        growth = self._to_float(row["Decadal popn growth rate % 2011/2001"])

        infrastructure = self.infrastructure_score(
            row,
        )

        return PopulationFeatures(
            ward_number=int(row["Ward_No"]),
            ward_name=row["Ward Name"],
            zone=row["BBMP Zone Name"],
            population=int(row["Population (2011)"]),
            area_sq_km=float(row["Area (sq km)"]),
            population_density=density,
            households=int(row["Households # (Census 2011)"]),
            road_length=float(row["Road Length (kms)"]),
            parks=int(row["Parks #"]),
            lakes=int(row["Lakes #"]),
            bus_stops=int(row["Bus Stops #"]),
            government_schools=int(row["Govt Schools #"]),
            police_stations=int(row["Police Stations #"]),
            fire_stations=int(row["Fire stations #"]),
            streetlights=int(row["Streetlights #"]),
            growth_rate=growth,
            infrastructure_score=infrastructure,
            population_category=self.classify_population(
                density,
            ),
        )

    # ======================================================
    # Dictionary
    # ======================================================

    @staticmethod
    def to_dict(
        population,
    ):

        return population.__dict__
