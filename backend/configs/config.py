"""
config.py

Central configuration file for the entire project.
"""

from pathlib import Path


# ==========================================================
# PROJECT PATHS
# ==========================================================

# config.py
#   ↓ parent
# configs/
#   ↓ parent
# backend/
#   ↓ parent
# Smart Urban Planning/

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = ROOT_DIR / "data"

IMAGE_DIR = DATA_DIR / "images"

LABEL_DIR = DATA_DIR / "label"

CHECKPOINT_DIR = ROOT_DIR / "checkpoints"

LOG_DIR = ROOT_DIR / "logs"


# ==========================================================
# DATASET
# ==========================================================

IMAGE_HEIGHT = 256

IMAGE_WIDTH = 256

IMAGE_CHANNELS = 3

NUM_CLASSES = 5

CLASS_NAMES = [
    "Background",
    "Road",
    "Building",
    "Vegetation",
    "Water",
]


# ==========================================================
# MODEL
# ==========================================================

MODEL_NAME = "AttentionResUNet"

BACKBONE = "Custom"

BASE_FILTERS = 32

DROPOUT_RATE = 0.2

L2_REGULARIZATION = 1e-4

USE_ATTENTION = True

USE_DEEP_SUPERVISION = False


# ==========================================================
# TRAINING
# ==========================================================

BATCH_SIZE = 8

EPOCHS = 100

LEARNING_RATE = 1e-4

RANDOM_SEED = 42

USE_MIXED_PRECISION = True


# ==========================================================
# DATA PIPELINE
# ==========================================================

SHUFFLE_BUFFER_SIZE = 1000

USE_CACHE = False

USE_PREFETCH = True

USE_AUGMENTATION = True


# ==========================================================
# CALLBACKS
# ==========================================================

EARLY_STOPPING_PATIENCE = 15

REDUCE_LR_PATIENCE = 5

MIN_LEARNING_RATE = 1e-6


# ==========================================================
# MODEL SAVING
# ==========================================================

BEST_MODEL_PATH = (
    CHECKPOINT_DIR / "best_model.keras"
)

FINAL_MODEL_PATH = (
    CHECKPOINT_DIR / "final_model.keras"
)


# ==========================================================
# INFERENCE
# ==========================================================

CONFIDENCE_THRESHOLD = 0.5