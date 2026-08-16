"""
utils.py

High-level prediction pipeline.

This module combines:
    - Predictor
    - Visualizer
    - Overlay Generator
    - Statistics Extractor

into a single interface.
"""

from backend.prediction.overlay import OverlayGenerator
from backend.prediction.predictor import Predictor
from backend.prediction.statistics import StatisticsExtractor
from backend.prediction.visualize import Visualizer


class PredictionPipeline:
    """
    Complete prediction pipeline.
    """

    def __init__(
        self,
        model_path,
        overlay_alpha=0.4,
    ):

        self.predictor = Predictor(model_path)

        self.visualizer = Visualizer()

        self.overlay = OverlayGenerator(
            alpha=overlay_alpha,
        )

        self.statistics = StatisticsExtractor()

    # ======================================================
    # Run Pipeline
    # ======================================================

    def run(
        self,
        image_path,
    ):
        """
        Executes the complete prediction pipeline.

        Returns
        -------
        dict
        """

        # -----------------------------
        # Prediction
        # -----------------------------

        original_image, predicted_mask = self.predictor.predict_image(
            image_path,
        )

        # -----------------------------
        # Colorize
        # -----------------------------

        colored_mask = self.visualizer.colorize(
            predicted_mask,
        )

        # -----------------------------
        # Overlay
        # -----------------------------

        overlay_image = self.overlay.overlay(
            original_image,
            colored_mask,
        )

        # -----------------------------
        # Statistics
        # -----------------------------

        statistics = self.statistics.extract(
            predicted_mask,
        )

        # -----------------------------
        # Return Everything
        # -----------------------------

        return {
            "original_image": original_image,
            "predicted_mask": predicted_mask,
            "colored_mask": colored_mask,
            "overlay_image": overlay_image,
            "statistics": statistics,
        }
