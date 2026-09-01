"""
trainer.py

Training pipeline for Attention ResUNet.

Supports:
- Model compilation
- Training
- Early stopping
- Best model checkpointing
- Automatic training resume after interruption
"""

from pathlib import Path

import tensorflow as tf

from backend.configs.config import EPOCHS, FINAL_MODEL_PATH
from backend.data_pipeline.dataset import get_train_dataset, get_validation_dataset
from backend.losses.factory import get_loss
from backend.metrics.factory import get_metrics
from backend.model.factory import build_model
from backend.training.callbacks import get_callbacks
from backend.training.optimizer import get_optimizer

# ==========================================================
# Training Backup
# ==========================================================

# Use a fresh backup directory for the resumed training run.
# The previous backup is kept untouched as a safety copy.
BACKUP_DIR = Path("checkpoints/training_backup_resume")


class Trainer:

    def __init__(self):

        self.model = build_model()

        self.optimizer = get_optimizer()

        self.loss = get_loss()

        self.metrics = get_metrics()

        self.callbacks = get_callbacks()

        self.train_dataset = get_train_dataset()

        self.validation_dataset = get_validation_dataset()

        self._add_backup_callback()

    # ======================================================
    # Backup / Resume
    # ======================================================

    def _add_backup_callback(self):

        BACKUP_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_callback = tf.keras.callbacks.BackupAndRestore(
            backup_dir=str(BACKUP_DIR),
            save_freq="epoch",
            delete_checkpoint=False,
        )

        self.callbacks.append(backup_callback)

    # ======================================================
    # Compile
    # ======================================================

    def compile(self):

        self.model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=self.metrics,
        )

    # ======================================================
    # Train
    # ======================================================

    def train(self):

        self.compile()

        print()
        print("=" * 60)
        print("Starting Attention ResUNet training")
        print("=" * 60)

        print(f"Maximum epochs: {EPOCHS}")

        print(f"Training backup: {BACKUP_DIR}")

        print("Training can be safely interrupted and resumed.")

        print("=" * 60)
        print()

        history = self.model.fit(
            self.train_dataset,
            validation_data=self.validation_dataset,
            epochs=EPOCHS,
            callbacks=self.callbacks,
            verbose=1,
        )

        # ==================================================
        # Save Final Model
        # ==================================================

        final_model_path = Path(FINAL_MODEL_PATH)

        final_model_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.model.save(final_model_path)

        print()
        print("=" * 60)
        print("Training completed successfully.")
        print(f"Final model saved to: {final_model_path}")
        print("=" * 60)

        return history

    # ======================================================
    # Summary
    # ======================================================

    def summary(self):

        self.model.summary()
