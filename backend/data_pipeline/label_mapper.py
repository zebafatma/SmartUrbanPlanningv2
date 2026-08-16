"""
label_mapper.py

Maps OpenEarthMap classes
to Smart Urban Planner classes.
"""

from enum import IntEnum

import numpy as np

# ==========================================================
# OpenEarthMap Classes
# ==========================================================


class OEMClass(IntEnum):
    UNKNOWN = 0
    BARELAND = 1
    RANGELAND = 2
    DEVELOPED_SPACE = 3
    ROAD = 4
    TREE = 5
    WATER = 6
    AGRICULTURE = 7
    BUILDING = 8


# ==========================================================
# Project Classes
# ==========================================================


class UrbanClass(IntEnum):
    BACKGROUND = 0
    ROAD = 1
    BUILDING = 2
    VEGETATION = 3
    WATER = 4


# ==========================================================
# Class Names
# ==========================================================

CLASS_NAMES = {
    UrbanClass.BACKGROUND: "Background",
    UrbanClass.ROAD: "Road",
    UrbanClass.BUILDING: "Building",
    UrbanClass.VEGETATION: "Vegetation",
    UrbanClass.WATER: "Water",
}


# ==========================================================
# Color Palette (RGB)
# Used later for visualization
# ==========================================================

CLASS_COLORS = {
    UrbanClass.BACKGROUND: (0, 0, 0),
    UrbanClass.ROAD: (255, 255, 255),
    UrbanClass.BUILDING: (220, 20, 60),
    UrbanClass.VEGETATION: (34, 139, 34),
    UrbanClass.WATER: (30, 144, 255),
}


# ==========================================================
# Mapping Table
# ==========================================================

LABEL_MAPPING = np.array(
    [
        UrbanClass.BACKGROUND,  # Unknown
        UrbanClass.BACKGROUND,  # Bareland
        UrbanClass.BACKGROUND,  # Rangeland
        UrbanClass.BACKGROUND,  # Developed Space
        UrbanClass.ROAD,  # Road
        UrbanClass.VEGETATION,  # Tree
        UrbanClass.WATER,  # Water
        UrbanClass.VEGETATION,  # Agriculture
        UrbanClass.BUILDING,  # Building
    ],
    dtype=np.uint8,
)


# ==========================================================
# Label Mapping
# ==========================================================


def map_labels(mask: np.ndarray) -> np.ndarray:
    """
    Convert OpenEarthMap labels (0-8)
    into project labels (0-4).

    Parameters
    ----------
    mask : np.ndarray

    Returns
    -------
    np.ndarray
    """

    if not isinstance(mask, np.ndarray):
        raise TypeError("Mask must be a NumPy array.")

    if mask.ndim != 2:
        raise ValueError("Mask must be a single-channel image.")

    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)

    max_label = int(mask.max())

    if max_label >= len(LABEL_MAPPING):
        raise ValueError(f"Invalid class id found: {max_label}")

    return LABEL_MAPPING[mask]


# ==========================================================
# Utility Functions
# ==========================================================


def get_class_names():
    """
    Returns project class names.
    """
    return CLASS_NAMES.copy()


def get_class_colors():
    """
    Returns RGB color palette.
    """
    return CLASS_COLORS.copy()


def get_mapping():
    """
    Returns mapping table.
    """
    return LABEL_MAPPING.copy()


def get_num_classes():
    """
    Returns number of classes.
    """
    return len(UrbanClass)
