"""
callbacks.py

Training callbacks.
"""

from tensorflow.keras.callbacks import (
    CSVLogger,
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard,
)

from backend.configs.config import (
    BEST_MODEL_PATH,
    EARLY_STOPPING_PATIENCE,
    LOG_DIR,
    MIN_LEARNING_RATE,
    REDUCE_LR_PATIENCE,
)


def get_callbacks():

    callbacks = [
        ModelCheckpoint(
            filepath=BEST_MODEL_PATH,
            monitor="val_loss",
            save_best_only=True,
            verbose=1,
        ),
        EarlyStopping(
            monitor="val_loss",
            patience=EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=REDUCE_LR_PATIENCE,
            min_lr=MIN_LEARNING_RATE,
            verbose=1,
        ),
        TensorBoard(
            log_dir=LOG_DIR,
            histogram_freq=1,
        ),
        CSVLogger(
            LOG_DIR / "training_log.csv",
            append=False,
        ),
    ]

    return callbacks
