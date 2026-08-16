"""
overlay.py

Creates an overlay by blending the original image
with the predicted segmentation mask.
"""

import cv2
import numpy as np


class OverlayGenerator:
    """
    Generates overlay images for visualization.
    """

    def __init__(self, alpha=0.4):
        """
        Parameters
        ----------
        alpha : float

            Transparency of segmentation mask.

            0.0 -> Only original image

            1.0 -> Only segmentation mask
        """

        if not (0.0 <= alpha <= 1.0):
            raise ValueError("Alpha must be between 0 and 1.")

        self.alpha = alpha

    # ======================================================
    # Resize Mask
    # ======================================================

    def resize_mask(
        self,
        mask,
        target_shape,
    ):
        """
        Resize colored mask to original image size.
        """

        height, width = target_shape[:2]

        return cv2.resize(
            mask,
            (width, height),
            interpolation=cv2.INTER_NEAREST,
        )

    # ======================================================
    # Overlay
    # ======================================================

    def overlay(
        self,
        original,
        colored_mask,
    ):
        """
        Blend original image and segmentation mask.

        Parameters
        ----------
        original : np.ndarray

            Original RGB image.

        colored_mask : np.ndarray

            RGB segmentation mask.

        Returns
        -------
        np.ndarray

            Overlay image.
        """

        if original.shape[:2] != colored_mask.shape[:2]:

            colored_mask = self.resize_mask(
                colored_mask,
                original.shape,
            )

        overlay = cv2.addWeighted(
            original,
            1 - self.alpha,
            colored_mask,
            self.alpha,
            0,
        )

        return overlay.astype(np.uint8)

    # ======================================================
    # Change Transparency
    # ======================================================

    def set_alpha(
        self,
        alpha,
    ):
        """
        Update transparency.
        """

        if not (0 <= alpha <= 1):
            raise ValueError("Alpha must be between 0 and 1.")

        self.alpha = alpha
