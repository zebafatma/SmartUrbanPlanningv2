"""
weather.py

Weather analysis module.
"""

from dataclasses import dataclass

import pandas as pd

from backend.recommendation.data_loader import ExternalDataLoader

# ==========================================================
# Weather Features
# ==========================================================


@dataclass
class WeatherFeatures:

    date: str

    average_temperature: float

    minimum_temperature: float

    maximum_temperature: float

    rainfall: float

    wind_speed: float

    pressure: float

    weather_category: str

    heat_risk: str


# ==========================================================
# Weather Analyzer
# ==========================================================


class WeatherAnalyzer:

    def __init__(self):

        self.loader = ExternalDataLoader()

        self.df = self.loader.load_weather()

        self.df["date"] = pd.to_datetime(self.df["date"])

    # ======================================================
    # Latest Weather
    # ======================================================

    def latest(self):

        row = self.df.sort_values("date").iloc[-1]

        return self._build_features(
            row,
        )

    # ======================================================
    # Weather By Date
    # ======================================================

    def by_date(
        self,
        date,
    ):

        row = self.df[self.df["date"] == pd.to_datetime(date)]

        if row.empty:

            raise ValueError(f"No weather data for {date}")

        return self._build_features(row.iloc[0])

    # ======================================================
    # Build Features
    # ======================================================

    def _build_features(
        self,
        row,
    ):

        rainfall = 0.0 if pd.isna(row["prcp"]) else float(row["prcp"])

        wind_speed = 0.0 if pd.isna(row["wspd"]) else float(row["wspd"])

        pressure = 0.0 if pd.isna(row["pres"]) else float(row["pres"])

        average_temp = float(row["tavg"])

        return WeatherFeatures(
            date=row["date"].strftime("%Y-%m-%d"),
            average_temperature=average_temp,
            minimum_temperature=float(row["tmin"]),
            maximum_temperature=float(row["tmax"]),
            rainfall=rainfall,
            wind_speed=wind_speed,
            pressure=pressure,
            weather_category=self.weather_category(
                rainfall,
                average_temp,
            ),
            heat_risk=self.heat_risk(
                average_temp,
            ),
        )

    # ======================================================
    # Weather Category
    # ======================================================

    @staticmethod
    def weather_category(
        rainfall,
        temperature,
    ):

        if rainfall > 25:

            return "Heavy Rain"

        elif rainfall > 5:

            return "Rainy"

        elif temperature > 35:

            return "Hot"

        elif temperature < 15:

            return "Cold"

        return "Pleasant"

    # ======================================================
    # Heat Risk
    # ======================================================

    @staticmethod
    def heat_risk(
        temperature,
    ):

        if temperature >= 38:

            return "Extreme"

        elif temperature >= 34:

            return "High"

        elif temperature >= 30:

            return "Moderate"

        return "Low"

    # ======================================================
    # Dictionary
    # ======================================================

    @staticmethod
    def to_dict(
        weather,
    ):

        return weather.__dict__
