"""
visualize.py

Converts predicted class masks into RGB images.
"""

import numpy as np

from backend.data_pipeline.label_mapper import get_class_colors


class Visualizer:
    """
    Converts segmentation masks into RGB images.
    """

    def __init__(self):

        self.colors = get_class_colors()

    # ======================================================
    # Color Mask
    # ======================================================

    def colorize(self, mask):
        """
        Converts a class mask into an RGB image.

        Parameters
        ----------
        mask : np.ndarray

            Shape:
                (H, W)

            Values:
                0 - Background
                1 - Road
                2 - Building
                3 - Vegetation
                4 - Water

        Returns
        -------
        np.ndarray

            RGB image
        """

        if mask.ndim != 2:
            raise ValueError("Mask must be 2-dimensional.")

        height, width = mask.shape

        colored = np.zeros(
            (
                height,
                width,
                3,
            ),
            dtype=np.uint8,
        )

        for class_id, color in self.colors.items():

            colored[mask == int(class_id)] = color

        return colored

    # ======================================================
    # Legend
    # ======================================================

    def get_colors(self):
        """
        Returns color mapping.
        """

        return self.colors
