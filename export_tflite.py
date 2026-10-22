"""
export_tflite.py

Converts checkpoints/best_model.keras to checkpoints/best_model.tflite.

The API automatically uses the .tflite file when it exists. It gives the
same predictions as the Keras model but runs with the small LiteRT runtime
instead of full TensorFlow, so the backend fits in 512 MB of memory.

Run after retraining:  python export_tflite.py
"""

import tensorflow as tf

from backend.configs.config import BEST_MODEL_PATH, TFLITE_MODEL_PATH


def main():

    model = tf.keras.models.load_model(BEST_MODEL_PATH, compile=False)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)

    TFLITE_MODEL_PATH.write_bytes(converter.convert())

    print(f"Saved {TFLITE_MODEL_PATH}")


if __name__ == "__main__":

    main()
