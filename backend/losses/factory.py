"""
factory.py

Returns training loss.
"""

from backend.losses.combined import combined_loss


def get_loss():

    return combined_loss
