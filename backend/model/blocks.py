"""
blocks.py

Reusable building blocks for Attention ResUNet.

Contains:

- Conv Block
- Residual Block
- SE Block
- Attention Gate
- Encoder Block
- Decoder Block
- Bottleneck
"""

import tensorflow as tf
from tensorflow.keras.initializers import HeNormal
from tensorflow.keras.layers import (
    Activation,
    Add,
    BatchNormalization,
    Concatenate,
    Conv2D,
    Conv2DTranspose,
    Dense,
    Dropout,
    GlobalAveragePooling2D,
    Input,
    MaxPooling2D,
    Multiply,
    Reshape,
)
from tensorflow.keras.regularizers import l2

from backend.configs.config import DROPOUT_RATE, L2_REGULARIZATION

KERNEL_INITIALIZER = HeNormal()


# ==========================================================
# Convolution Block
# ==========================================================


def conv_block(
    x,
    filters,
    kernel_size=3,
):

    x = Conv2D(
        filters,
        kernel_size,
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
        kernel_regularizer=l2(L2_REGULARIZATION),
        use_bias=False,
    )(x)

    x = BatchNormalization()(x)

    x = Activation("relu")(x)

    return x


# ==========================================================
# Double Convolution
# ==========================================================


def double_conv_block(
    x,
    filters,
):

    x = conv_block(
        x,
        filters,
    )

    x = conv_block(
        x,
        filters,
    )

    return x


# ==========================================================
# Residual Block
# ==========================================================


def residual_block(
    x,
    filters,
):

    shortcut = Conv2D(
        filters,
        1,
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
        kernel_regularizer=l2(L2_REGULARIZATION),
        use_bias=False,
    )(x)

    shortcut = BatchNormalization()(shortcut)

    x = conv_block(
        x,
        filters,
    )

    x = Dropout(DROPOUT_RATE)(x)

    x = conv_block(
        x,
        filters,
    )

    x = Add()(
        [
            x,
            shortcut,
        ]
    )

    x = Activation("relu")(x)

    return x


# ==========================================================
# Squeeze and Excitation Block
# ==========================================================


def se_block(
    x,
    reduction=16,
):
    """
    Squeeze-and-Excitation Block

    Learns channel-wise attention.
    """

    filters = x.shape[-1]

    se = GlobalAveragePooling2D()(x)

    se = Dense(
        filters // reduction,
        activation="relu",
        kernel_initializer=KERNEL_INITIALIZER,
    )(se)

    se = Dense(
        filters,
        activation="sigmoid",
        kernel_initializer=KERNEL_INITIALIZER,
    )(se)

    se = Reshape((1, 1, filters))(se)

    x = Multiply()(
        [
            x,
            se,
        ]
    )

    return x


# ==========================================================
# Attention Gate
# ==========================================================


def attention_gate(
    encoder_features,
    decoder_features,
    filters,
):
    """
    Attention Gate

    Encoder features are filtered before
    being concatenated with decoder features.
    """

    theta_x = Conv2D(
        filters,
        kernel_size=1,
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
        use_bias=False,
    )(encoder_features)

    theta_x = BatchNormalization()(theta_x)

    phi_g = Conv2D(
        filters,
        kernel_size=1,
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
        use_bias=False,
    )(decoder_features)

    phi_g = BatchNormalization()(phi_g)

    attention = Add()(
        [
            theta_x,
            phi_g,
        ]
    )

    attention = Activation("relu")(attention)

    attention = Conv2D(
        1,
        kernel_size=1,
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
        activation="sigmoid",
    )(attention)

    gated = Multiply()(
        [
            encoder_features,
            attention,
        ]
    )

    return gated


# ==========================================================
# Encoder Block
# ==========================================================


def encoder_block(
    x,
    filters,
):
    """
    Encoder

    Returns:
        skip connection
        pooled output
    """

    x = residual_block(
        x,
        filters,
    )

    x = se_block(
        x,
    )

    skip = x

    pool = MaxPooling2D(pool_size=(2, 2))(x)

    return skip, pool


# ==========================================================
# Bottleneck Block
# ==========================================================


def bottleneck_block(
    x,
    filters,
):
    """
    Bottleneck between encoder and decoder.
    """

    x = residual_block(
        x,
        filters,
    )

    x = se_block(
        x,
    )

    return x


# ==========================================================
# Decoder Block
# ==========================================================


def decoder_block(
    x,
    skip,
    filters,
    use_attention=True,
):
    """
    Decoder Block

    Steps:
        1. Upsample
        2. Attention Gate
        3. Concatenate
        4. Residual Block
        5. SE Block
    """

    x = Conv2DTranspose(
        filters,
        kernel_size=2,
        strides=2,
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
    )(x)

    if use_attention:

        skip = attention_gate(
            encoder_features=skip,
            decoder_features=x,
            filters=filters,
        )

    x = Concatenate()(
        [
            x,
            skip,
        ]
    )

    x = residual_block(
        x,
        filters,
    )

    x = se_block(
        x,
    )

    return x


# ==========================================================
# Output Block
# ==========================================================


def output_block(
    x,
    num_classes,
):
    """
    Final segmentation layer.
    """

    outputs = Conv2D(
        filters=num_classes,
        kernel_size=1,
        activation="softmax",
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
    )(x)

    return outputs


# ==========================================================
# Input Validation
# ==========================================================


def validate_filters(filters):
    """
    Ensure the number of filters is valid.
    """

    if filters <= 0:
        raise ValueError("Number of filters must be greater than zero.")


# ==========================================================
# Utility Functions
# ==========================================================


def upsample(
    x,
    filters,
):
    """
    Upsampling layer used in decoder.
    """

    return Conv2DTranspose(
        filters=filters,
        kernel_size=2,
        strides=2,
        padding="same",
        kernel_initializer=KERNEL_INITIALIZER,
    )(x)


def downsample(
    x,
):
    """
    Downsampling layer used in encoder.
    """

    return MaxPooling2D(pool_size=(2, 2))(x)


# ==========================================================
# Exported Components
# ==========================================================

__all__ = [
    "conv_block",
    "double_conv_block",
    "residual_block",
    "se_block",
    "attention_gate",
    "encoder_block",
    "decoder_block",
    "bottleneck_block",
    "output_block",
    "upsample",
    "downsample",
]
