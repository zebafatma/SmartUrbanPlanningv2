"""
predictor.py

Loads a trained model and performs semantic segmentation
on a satellite image.
"""

from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf

from backend.configs.config import IMAGE_HEIGHT, IMAGE_WIDTH
from backend.data_pipeline.preprocessing import preprocess_image


class Predictor:
    """
    Semantic segmentation predictor.
    """

    def __init__(self, model_path):

        self.model_path = Path(model_path)

        self.model = self._load_model()

    # ======================================================
    # Load Model
    # ======================================================

    def _load_model(self):
        """
        Loads the trained Keras model.
        """

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found:\n{self.model_path}")

        model = tf.keras.models.load_model(
            self.model_path,
            compile=False,
        )

        return model

    # ======================================================
    # Read Image
    # ======================================================

    def read_image(self, image_path):
        """
        Reads an RGB image.
        """

        image_path = Path(image_path)

        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(f"Cannot read image:\n{image_path}")

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        return image

    # ======================================================
    # Prepare Image
    # ======================================================

    def prepare_image(self, image):
        """
        Preprocess image for prediction.
        """

        original = image.copy()

        image = preprocess_image(image)

        image = np.expand_dims(
            image,
            axis=0,
        )

        return original, image

    # ======================================================
    # Predict
    # ======================================================

    def predict(self, image):
        """
        Predict segmentation mask.
        """

        prediction = self.model.predict(
            image,
            verbose=0,
        )

        prediction = np.argmax(
            prediction,
            axis=-1,
        )

        prediction = prediction[0]

        return prediction.astype(np.uint8)

    # ======================================================
    # Complete Pipeline
    # ======================================================

    def predict_image(self, image_path):
        """
        Runs complete prediction pipeline.
        """

        image = self.read_image(
            image_path,
        )

        original, processed = self.prepare_image(
            image,
        )

        prediction = self.predict(
            processed,
        )

        return original, prediction
