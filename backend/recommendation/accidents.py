"""
accidents.py

Road accident analysis module.
"""

from dataclasses import dataclass

import pandas as pd

from backend.recommendation.data_loader import ExternalDataLoader

# ==========================================================
# Accident Features
# ==========================================================


@dataclass
class AccidentFeatures:

    year: int

    fatal_accidents: int

    fatalities: int

    non_fatal_accidents: int

    total_accidents: int

    accident_severity_index: float

    safety_category: str

    yearly_change: float


# ==========================================================
# Accident Analyzer
# ==========================================================


class AccidentAnalyzer:

    def __init__(self):

        self.loader = ExternalDataLoader()

        self.df = self.loader.load_accidents()

        self.df["Total"] = self.df["Total"].astype(str).str.replace(",", "").astype(int)

        self.df["Non-Fatal Road Accidents"] = (
            self.df["Non-Fatal Road Accidents"]
            .astype(str)
            .str.replace(",", "")
            .astype(int)
        )

    # ======================================================
    # Severity Index
    # ======================================================

    @staticmethod
    def severity_index(row):

        return round(
            (row["Killed"] / row["Total"]) * 100,
            2,
        )

    # ======================================================
    # Safety Category
    # ======================================================

    @staticmethod
    def classify(severity):

        if severity < 10:

            return "Safe"

        elif severity < 15:

            return "Moderate"

        elif severity < 20:

            return "Risky"

        return "Critical"

    # ======================================================
    # Latest Year
    # ======================================================

    def latest(self):

        row = self.df.sort_values("Year").iloc[-1]

        return self._build_features(row)

    # ======================================================
    # By Year
    # ======================================================

    def by_year(
        self,
        year,
    ):

        row = self.df[self.df["Year"] == year]

        if row.empty:

            raise ValueError(f"No data found for {year}")

        return self._build_features(row.iloc[0])

    # ======================================================
    # Build Features
    # ======================================================

    def _build_features(
        self,
        row,
    ):

        severity = self.severity_index(row)

        previous = self.df[self.df["Year"] == row["Year"] - 1]

        if previous.empty:

            yearly_change = 0.0

        else:

            previous_total = previous.iloc[0]["Total"]

            yearly_change = round(
                ((row["Total"] - previous_total) / previous_total) * 100,
                2,
            )

        return AccidentFeatures(
            year=int(row["Year"]),
            fatal_accidents=int(row["Fatal Road Accidents"]),
            fatalities=int(row["Killed"]),
            non_fatal_accidents=int(row["Non-Fatal Road Accidents"]),
            total_accidents=int(row["Total"]),
            accident_severity_index=severity,
            safety_category=self.classify(severity),
            yearly_change=yearly_change,
        )

    # ======================================================
    # Dictionary
    # ======================================================

    @staticmethod
    def to_dict(
        accident,
    ):

        return accident.__dict__
