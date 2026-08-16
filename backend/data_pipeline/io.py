"""
io.py

Responsible for reading images and masks from disk.

Supports:
    - GeoTIFF (.tif/.tiff)
    - PNG
    - JPG
    - JPEG
"""

from pathlib import Path

import cv2
import numpy as np
import rasterio

SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
}


# ==========================================================
# Utility
# ==========================================================


def is_image_file(file_name: str | Path) -> bool:
    """
    Check if file is a supported image.
    """

    return Path(file_name).suffix.lower() in SUPPORTED_EXTENSIONS


# ==========================================================
# Read RGB Image
# ==========================================================


def read_image(image_path: str | Path) -> np.ndarray:
    """
    Reads an RGB satellite image.

    Returns
    -------
    np.ndarray

        Shape:
            (H,W,3)

        dtype:
            uint8
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found:\n{image_path}")

    extension = image_path.suffix.lower()

    # ------------------------------------------------------
    # GeoTIFF
    # ------------------------------------------------------

    if extension in {".tif", ".tiff"}:

        with rasterio.open(image_path) as src:

            image = src.read()

            image = np.moveaxis(
                image,
                0,
                -1,
            )

            if image.shape[-1] > 3:
                image = image[:, :, :3]

            image = image.astype(np.uint8)

            return image

    # ------------------------------------------------------
    # PNG / JPG
    # ------------------------------------------------------

    image = cv2.imread(
        str(image_path),
        cv2.IMREAD_COLOR,
    )

    if image is None:
        raise ValueError(f"Unable to read image:\n{image_path}")

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB,
    )

    return image


# ==========================================================
# Read Segmentation Mask
# ==========================================================


def read_mask(mask_path: str | Path) -> np.ndarray:
    """
    Reads segmentation mask.

    Returns
    -------
    np.ndarray

        Shape:
            (H,W)

        dtype:
            uint8
    """

    mask_path = Path(mask_path)

    if not mask_path.exists():
        raise FileNotFoundError(f"Mask not found:\n{mask_path}")

    extension = mask_path.suffix.lower()

    # ------------------------------------------------------
    # GeoTIFF Mask
    # ------------------------------------------------------

    if extension in {".tif", ".tiff"}:

        with rasterio.open(mask_path) as src:

            mask = src.read(1)

            return mask.astype(np.uint8)

    # ------------------------------------------------------
    # PNG Mask
    # ------------------------------------------------------

    mask = cv2.imread(
        str(mask_path),
        cv2.IMREAD_GRAYSCALE,
    )

    if mask is None:
        raise ValueError(f"Unable to read mask:\n{mask_path}")

    return mask.astype(np.uint8)


# ==========================================================
# Read Image + Mask
# ==========================================================


def load_sample(
    image_path: str | Path,
    mask_path: str | Path,
):
    """
    Loads one training sample.

    Returns
    -------
    image, mask
    """

    image = read_image(image_path)

    mask = read_mask(mask_path)

    return image, mask
