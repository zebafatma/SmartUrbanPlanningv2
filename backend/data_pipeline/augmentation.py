"""
augmentation.py

Albumentations pipeline for semantic segmentation.

The exact same geometric transformation is applied
to both image and mask.
"""

import albumentations as A
import cv2

from backend.configs.config import IMAGE_HEIGHT, IMAGE_WIDTH, USE_AUGMENTATION

# ==========================================================
# Training Augmentation
# ==========================================================


def get_training_augmentation():
    """
    Returns augmentation pipeline used during training.
    """

    if not USE_AUGMENTATION:

        return A.Compose(
            [
                A.Resize(
                    IMAGE_HEIGHT,
                    IMAGE_WIDTH,
                )
            ]
        )

    return A.Compose(
        [
            # -------------------------
            # Geometric
            # -------------------------
            A.HorizontalFlip(
                p=0.5,
            ),
            A.VerticalFlip(
                p=0.2,
            ),
            A.RandomRotate90(
                p=0.5,
            ),
            A.ShiftScaleRotate(
                shift_limit=0.10,
                scale_limit=0.10,
                rotate_limit=20,
                interpolation=cv2.INTER_LINEAR,
                border_mode=cv2.BORDER_CONSTANT,
                p=0.5,
            ),
            # -------------------------
            # Color
            # -------------------------
            A.RandomBrightnessContrast(
                brightness_limit=0.20,
                contrast_limit=0.20,
                p=0.5,
            ),
            A.RandomGamma(
                gamma_limit=(80, 120),
                p=0.3,
            ),
            A.CLAHE(
                clip_limit=2,
                tile_grid_size=(8, 8),
                p=0.3,
            ),
            # -------------------------
            # Noise
            # -------------------------
            A.GaussNoise(
                std_range=(0.01, 0.05),
                p=0.2,
            ),
            # -------------------------
            # Final Resize
            # -------------------------
            A.Resize(
                IMAGE_HEIGHT,
                IMAGE_WIDTH,
            ),
        ]
    )


# ==========================================================
# Validation
# ==========================================================


def get_validation_augmentation():
    """
    Validation should not contain
    random transformations.
    """

    return A.Compose(
        [
            A.Resize(
                IMAGE_HEIGHT,
                IMAGE_WIDTH,
            )
        ]
    )


# ==========================================================
# Apply Augmentation
# ==========================================================


def augment(
    image,
    mask,
    train=True,
):
    """
    Apply augmentation.

    Parameters
    ----------
    image : np.ndarray

    mask : np.ndarray

    train : bool

    Returns
    -------
    image
    mask
    """

    if train:

        transform = get_training_augmentation()

    else:

        transform = get_validation_augmentation()

    augmented = transform(
        image=image,
        mask=mask,
    )

    return (
        augmented["image"],
        augmented["mask"],
    )
