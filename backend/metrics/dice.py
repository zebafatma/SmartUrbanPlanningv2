"""
dice.py

Dice Score metric.

Unlike Dice Loss,
higher is better.
"""

import tensorflow as tf


class DiceScore(tf.keras.metrics.Metric):

    def __init__(
        self,
        name="dice_score",
        smooth=1e-6,
        **kwargs,
    ):
        super().__init__(
            name=name,
            **kwargs,
        )

        self.smooth = smooth

        self.total = self.add_weight(
            name="total",
            initializer="zeros",
        )

        self.count = self.add_weight(
            name="count",
            initializer="zeros",
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

        num_classes = tf.shape(y_pred)[-1]

        y_true = tf.one_hot(
            y_true,
            depth=num_classes,
        )

        y_pred = tf.cast(
            y_pred,
            tf.float32,
        )

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

        denominator = tf.reduce_sum(
            y_true,
            axis=0,
        ) + tf.reduce_sum(
            y_pred,
            axis=0,
        )

        dice = (2.0 * intersection + self.smooth) / (denominator + self.smooth)

        self.total.assign_add(tf.reduce_mean(dice))

        self.count.assign_add(1)

    def result(self):

        return self.total / self.count

    def reset_state(self):

        self.total.assign(0.0)

        self.count.assign(0.0)
