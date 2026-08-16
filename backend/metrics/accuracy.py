"""
accuracy.py
"""

import tensorflow as tf


def get_accuracy():

    return tf.keras.metrics.SparseCategoricalAccuracy(
        name="accuracy",
    )
