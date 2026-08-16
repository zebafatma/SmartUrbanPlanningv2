"""
factory.py

Model Factory
"""

from backend.model.architecture import build_attention_resunet


def build_model():
    """
    Returns the segmentation model.
    """

    return build_attention_resunet()
