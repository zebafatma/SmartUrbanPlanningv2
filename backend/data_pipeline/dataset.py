"""
dataset.py

TensorFlow Dataset pipeline for semantic segmentation.
"""

from pathlib import Path

import numpy as np
import tensorflow as tf

from backend.configs.config import (BATCH_SIZE, IMAGE_CHANNELS, IMAGE_HEIGHT,
                            IMAGE_WIDTH, SHUFFLE_BUFFER_SIZE, USE_CACHE,
                            USE_PREFETCH)
from backend.data_pipeline.augmentation import augment
from backend.data_pipeline.io import load_sample
from backend.data_pipeline.preprocessing import preprocess_sample

AUTOTUNE = tf.data.AUTOTUNE


# ==========================================================
# Python Loader
# ==========================================================


def _load_data(image_path, mask_path, train):

    image_path = image_path.decode("utf-8")
    mask_path = mask_path.decode("utf-8")

    image, mask = load_sample(
        image_path,
        mask_path,
    )

    image, mask = preprocess_sample(
        image,
        mask,
    )

    image, mask = augment(
        image,
        mask,
        train=train,
    )

    image = image.astype(np.float32)
    mask = mask.astype(np.uint8)

    return image, mask


# ==========================================================
# TensorFlow Wrapper
# ==========================================================


def _tf_wrapper(
    image_path,
    mask_path,
    train,
):

    image, mask = tf.numpy_function(
        func=lambda x, y: _load_data(
            x,
            y,
            train,
        ),
        inp=[
            image_path,
            mask_path,
        ],
        Tout=[
            tf.float32,
            tf.uint8,
        ],
    )

    image.set_shape(
        (
            IMAGE_HEIGHT,
            IMAGE_WIDTH,
            IMAGE_CHANNELS,
        )
    )

    mask.set_shape(
        (
            IMAGE_HEIGHT,
            IMAGE_WIDTH,
        )
    )

    return image, mask


# ==========================================================
# Create Dataset
# ==========================================================


def create_dataset(
    image_dir,
    mask_dir,
    train=True,
):

    image_dir = Path(image_dir)
    mask_dir = Path(mask_dir)

    image_paths = sorted([str(file) for file in image_dir.iterdir() if file.is_file()])

    mask_paths = sorted([str(file) for file in mask_dir.iterdir() if file.is_file()])

    if len(image_paths) != len(mask_paths):

        raise ValueError("Number of images and masks do not match.")

    dataset = tf.data.Dataset.from_tensor_slices(
        (
            image_paths,
            mask_paths,
        )
    )

    if train:

        dataset = dataset.shuffle(
            SHUFFLE_BUFFER_SIZE,
            reshuffle_each_iteration=True,
        )

    dataset = dataset.map(
        lambda image, mask: _tf_wrapper(
            image,
            mask,
            train,
        ),
        num_parallel_calls=AUTOTUNE,
    )

    if USE_CACHE:

        dataset = dataset.cache()

    dataset = dataset.batch(
        BATCH_SIZE,
        drop_remainder=False,
    )

    if USE_PREFETCH:

        dataset = dataset.prefetch(
            AUTOTUNE,
        )

    return dataset


# ==========================================================
# Convenience Functions
# ==========================================================


def get_train_dataset():

    from backend.configs.config import IMAGE_DIR, LABEL_DIR

    return create_dataset(
        IMAGE_DIR / "train",
        LABEL_DIR / "train",
        train=True,
    )


def get_validation_dataset():

    from backend.configs.config import IMAGE_DIR, LABEL_DIR

    return create_dataset(
        IMAGE_DIR / "val",
        LABEL_DIR / "val",
        train=False,
    )
