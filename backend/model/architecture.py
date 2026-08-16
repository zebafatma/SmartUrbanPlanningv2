"""
architecture.py

Attention ResUNet Architecture
"""

from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model

from backend.configs.config import (BASE_FILTERS, IMAGE_CHANNELS, IMAGE_HEIGHT,
                            IMAGE_WIDTH, NUM_CLASSES, USE_ATTENTION)
from backend.model.blocks import (bottleneck_block, decoder_block, encoder_block,
                          output_block)


def build_attention_resunet():
    """
    Builds the complete Attention ResUNet model.

    Returns
    -------
    tf.keras.Model
    """

    inputs = Input(
        shape=(
            IMAGE_HEIGHT,
            IMAGE_WIDTH,
            IMAGE_CHANNELS,
        ),
        name="input_image",
    )

    # ======================================================
    # Encoder
    # ======================================================

    skip1, pool1 = encoder_block(
        inputs,
        BASE_FILTERS,
    )

    skip2, pool2 = encoder_block(
        pool1,
        BASE_FILTERS * 2,
    )

    skip3, pool3 = encoder_block(
        pool2,
        BASE_FILTERS * 4,
    )

    skip4, pool4 = encoder_block(
        pool3,
        BASE_FILTERS * 8,
    )

    # ======================================================
    # Bottleneck
    # ======================================================

    bridge = bottleneck_block(
        pool4,
        BASE_FILTERS * 16,
    )

    # ======================================================
    # Decoder
    # ======================================================

    decoder4 = decoder_block(
        bridge,
        skip4,
        BASE_FILTERS * 8,
        use_attention=USE_ATTENTION,
    )

    decoder3 = decoder_block(
        decoder4,
        skip3,
        BASE_FILTERS * 4,
        use_attention=USE_ATTENTION,
    )

    decoder2 = decoder_block(
        decoder3,
        skip2,
        BASE_FILTERS * 2,
        use_attention=USE_ATTENTION,
    )

    decoder1 = decoder_block(
        decoder2,
        skip1,
        BASE_FILTERS,
        use_attention=USE_ATTENTION,
    )

    # ======================================================
    # Output
    # ======================================================

    outputs = output_block(
        decoder1,
        NUM_CLASSES,
    )

    model = Model(
        inputs=inputs,
        outputs=outputs,
        name="AttentionResUNet",
    )

    return model


def get_model():
    """
    Returns the model instance.
    """

    return build_attention_resunet()
