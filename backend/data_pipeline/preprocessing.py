"""
preprocessing.py

Image and mask preprocessing for semantic segmentation.
"""

import cv2
import numpy as np

from backend.configs.config import IMAGE_HEIGHT, IMAGE_WIDTH
from backend.data_pipeline.label_mapper import map_labels

# ==========================================================
# Validation
# ==========================================================


def validate_image(image: np.ndarray) -> None:
    """
    Validate RGB image.
    """

    if image is None:
        raise ValueError("Image is None.")

    if not isinstance(image, np.ndarray):
        raise TypeError("Image must be a NumPy array.")

    if image.ndim != 3:
        raise ValueError(f"Expected RGB image. Got shape {image.shape}")

    if image.shape[-1] != 3:
        raise ValueError(f"Expected 3 channels. Got {image.shape[-1]}")


def validate_mask(mask: np.ndarray) -> None:
    """
    Validate segmentation mask.
    """

    if mask is None:
        raise ValueError("Mask is None.")

    if not isinstance(mask, np.ndarray):
        raise TypeError("Mask must be a NumPy array.")

    if mask.ndim != 2:
        raise ValueError(f"Expected grayscale mask. Got shape {mask.shape}")


# ==========================================================
# Resize
# ==========================================================


def resize_image(image: np.ndarray) -> np.ndarray:
    """
    Resize RGB image.
    """

    return cv2.resize(
        image,
        (IMAGE_WIDTH, IMAGE_HEIGHT),
        interpolation=cv2.INTER_LINEAR,
    )


def resize_mask(mask: np.ndarray) -> np.ndarray:
    """
    Resize segmentation mask.

    IMPORTANT:
    Never use bilinear interpolation.
    """

    return cv2.resize(
        mask,
        (IMAGE_WIDTH, IMAGE_HEIGHT),
        interpolation=cv2.INTER_NEAREST,
    )


# ==========================================================
# Normalization
# ==========================================================


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize RGB image to [0,1].
    """

    image = image.astype(np.float32)

    image /= 255.0

    return image


# ==========================================================
# Complete Image Pipeline
# ==========================================================


def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Complete preprocessing for RGB image.
    """

    validate_image(image)

    image = resize_image(image)

    image = normalize_image(image)

    return image


# ==========================================================
# Complete Mask Pipeline
# ==========================================================


def preprocess_mask(mask: np.ndarray) -> np.ndarray:
    """
    Complete preprocessing for segmentation mask.
    """

    validate_mask(mask)

    mask = resize_mask(mask)

    mask = map_labels(mask)

    return mask.astype(np.uint8)


# ==========================================================
# Sample Pipeline
# ==========================================================


def preprocess_sample(
    image: np.ndarray,
    mask: np.ndarray,
):
    """
    Preprocess one training sample.
    """

    image = preprocess_image(image)

    mask = preprocess_mask(mask)

    return image, mask
