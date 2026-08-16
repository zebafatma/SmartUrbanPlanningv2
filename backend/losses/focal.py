"""
focal.py

Sparse Categorical Focal Loss

Works directly with integer masks.

No one-hot encoding required in the dataset.
"""

import tensorflow as tf


class SparseCategoricalFocalLoss(tf.keras.losses.Loss):

    def __init__(
        self,
        gamma=2.0,
        alpha=0.25,
        name="sparse_categorical_focal_loss",
    ):
        super().__init__(name=name)

        self.gamma = gamma
        self.alpha = alpha

    def call(self, y_true, y_pred):

        # Remove channel dimension if present
        if len(y_true.shape) == 4:
            y_true = tf.squeeze(y_true, axis=-1)

        y_true = tf.cast(y_true, tf.int32)

        # Convert labels to one-hot only for loss computation
        y_true_one_hot = tf.one_hot(
            y_true,
            depth=tf.shape(y_pred)[-1],
        )

        epsilon = tf.keras.backend.epsilon()

        y_pred = tf.clip_by_value(
            y_pred,
            epsilon,
            1.0 - epsilon,
        )

        cross_entropy = -(y_true_one_hot * tf.math.log(y_pred))

        focal_weight = self.alpha * tf.pow(
            1.0 - y_pred,
            self.gamma,
        )

        loss = focal_weight * cross_entropy

        return tf.reduce_mean(tf.reduce_sum(loss, axis=-1))
