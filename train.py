"""
train.py

Entry point for training.
"""

from backend.training.trainer import Trainer


def main():

    trainer = Trainer()

    trainer.summary()

    trainer.train()


if __name__ == "__main__":

    main()
