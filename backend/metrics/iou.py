"""
iou.py

Multi-class Mean IoU
"""

import tensorflow as tf


class MeanIoUMetric(tf.keras.metrics.MeanIoU):

    def __init__(
        self,
        num_classes=5,
        name="mean_iou",
    ):

        super().__init__(
            num_classes=num_classes,
            name=name,
        )

    def update_state(
        self,
        y_true,
        y_pred,
        sample_weight=None,
    ):

        if len(y_true.shape) == 4:
            y_true = tf.squeeze(
                y_true,
                axis=-1,
            )

        y_true = tf.cast(
            y_true,
            tf.int32,
        )

        y_pred = tf.argmax(
            y_pred,
            axis=-1,
            output_type=tf.int32,
        )

        return super().update_state(
            y_true,
            y_pred,
            sample_weight,
        )
