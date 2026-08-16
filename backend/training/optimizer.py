"""
optimizer.py
"""

import tensorflow as tf
from tensorflow.keras import mixed_precision

from backend.configs.config import LEARNING_RATE, USE_MIXED_PRECISION


def get_optimizer():

    if USE_MIXED_PRECISION:

        mixed_precision.set_global_policy("mixed_float16")

    optimizer = tf.keras.optimizers.AdamW(
        learning_rate=LEARNING_RATE,
        weight_decay=1e-4,
    )

    return optimizer
