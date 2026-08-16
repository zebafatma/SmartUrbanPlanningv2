"""
statistics.py

Extracts statistics from predicted segmentation masks.
"""

import numpy as np

from backend.data_pipeline.label_mapper import get_class_names


class StatisticsExtractor:
    """
    Computes statistics from a segmentation mask.
    """

    def __init__(self):

        self.class_names = get_class_names()

    # ======================================================
    # Pixel Counts
    # ======================================================

    def pixel_counts(
        self,
        mask: np.ndarray,
    ) -> dict:
        """
        Returns pixel count for each class.
        """

        counts = {}

        total_pixels = mask.size

        for class_id, class_name in self.class_names.items():

            pixels = int(np.sum(mask == int(class_id)))

            counts[class_name] = pixels

        counts["Total Pixels"] = int(total_pixels)

        return counts

    # ======================================================
    # Percentages
    # ======================================================

    def percentages(
        self,
        mask: np.ndarray,
    ) -> dict:
        """
        Returns percentage occupied by each class.
        """

        percentages = {}

        total_pixels = mask.size

        for class_id, class_name in self.class_names.items():

            pixels = np.sum(mask == int(class_id))

            percentages[class_name] = round(
                (pixels / total_pixels) * 100,
                2,
            )

        return percentages

    # ======================================================
    # Complete Statistics
    # ======================================================

    def extract(
        self,
        mask: np.ndarray,
    ) -> dict:
        """
        Returns complete statistics.
        """

        return {
            "pixel_counts": self.pixel_counts(mask),
            "percentages": self.percentages(mask),
        }

    # ======================================================
    # Pretty Print
    # ======================================================

    def print_statistics(
        self,
        statistics: dict,
    ) -> None:
        """
        Print statistics to console.
        """

        print("\n========== Pixel Counts ==========\n")

        for key, value in statistics["pixel_counts"].items():

            print(f"{key:<15}: {value}")

        print("\n========== Area Percentage ==========\n")

        for key, value in statistics["percentages"].items():

            print(f"{key:<15}: {value:.2f}%")
