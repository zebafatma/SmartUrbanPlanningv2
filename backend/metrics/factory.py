"""
factory.py

Returns all training metrics.
"""

from backend.metrics.accuracy import get_accuracy
from backend.metrics.dice import DiceScore
from backend.metrics.iou import MeanIoUMetric


def get_metrics():

    return [
        get_accuracy(),
        DiceScore(),
        MeanIoUMetric(),
    ]
