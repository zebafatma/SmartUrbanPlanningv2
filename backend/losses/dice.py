"""
dice.py

Multi-class Dice Loss

Accepts integer masks directly.
Internally converts them to one-hot encoding.
"""

import tensorflow as tf


def dice_loss(
    y_true,
    y_pred,
    smooth=1e-6,
):
    """
    Multi-class Dice Loss

    Parameters
    ----------
    y_true : Integer mask
             Shape:
             (B,H,W) or (B,H,W,1)

    y_pred : Softmax probabilities
             Shape:
             (B,H,W,C)
    """

    # Remove last dimension if present
    if len(y_true.shape) == 4:
        y_true = tf.squeeze(y_true, axis=-1)

    y_true = tf.cast(y_true, tf.int32)

    num_classes = tf.shape(y_pred)[-1]

    # Integer -> One-hot
    y_true = tf.one_hot(
        y_true,
        depth=num_classes,
        dtype=tf.float32,
    )

    y_pred = tf.cast(
        y_pred,
        tf.float32,
    )

    # Flatten
    y_true = tf.reshape(
        y_true,
        (-1, num_classes),
    )

    y_pred = tf.reshape(
        y_pred,
        (-1, num_classes),
    )

    intersection = tf.reduce_sum(
        y_true * y_pred,
        axis=0,
    )

    denominator = tf.reduce_sum(y_true, axis=0) + tf.reduce_sum(y_pred, axis=0)

    dice = (2.0 * intersection + smooth) / (denominator + smooth)

    dice = tf.reduce_mean(dice)

    return 1.0 - dice
