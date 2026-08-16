"""
combined.py

Final training loss.
"""

import tensorflow as tf

from backend.losses.dice import dice_loss
from backend.losses.focal import SparseCategoricalFocalLoss

focal = SparseCategoricalFocalLoss()


def combined_loss(y_true, y_pred):
    """
    Dice + Focal Loss
    """

    dice = dice_loss(
        y_true,
        y_pred,
    )

    focal_loss = focal(
        y_true,
        y_pred,
    )

    return dice + focal_loss
