"""
predictor.py

Loads a trained model and performs semantic segmentation
on a satellite image.
"""

from pathlib import Path

import cv2
import numpy as np

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
        Loads the trained model.

        - .tflite : TensorFlow Lite model, run with the lightweight LiteRT
                    runtime (ai-edge-litert). Used for deployment because it
                    needs a fraction of the memory of full TensorFlow.
        - .keras  : full Keras model (requires TensorFlow).
        """

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found:\n{self.model_path}")

        if self.model_path.suffix == ".tflite":
            return _TFLiteModel(self.model_path)

        import tensorflow as tf

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


class _TFLiteModel:
    """
    Minimal wrapper giving a TensorFlow Lite model the same
    predict() interface as a Keras model.
    """

    def __init__(self, model_path):

        try:
            from ai_edge_litert.interpreter import Interpreter
        except ImportError:
            # Fallback for environments with full TensorFlow
            # (e.g. Windows, where ai-edge-litert has no wheels).
            from tensorflow.lite import Interpreter

        self.interpreter = Interpreter(model_path=str(model_path))
        self.interpreter.allocate_tensors()

        self.input_index = self.interpreter.get_input_details()[0]["index"]
        self.output_index = self.interpreter.get_output_details()[0]["index"]

    def predict(self, images, verbose=0):

        outputs = []

        for image in images:
            self.interpreter.set_tensor(
                self.input_index,
                np.expand_dims(image, axis=0).astype(np.float32),
            )
            self.interpreter.invoke()
            outputs.append(self.interpreter.get_tensor(self.output_index)[0])

        return np.stack(outputs)
