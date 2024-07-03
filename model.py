import numpy as np
import os
import pandas as pd
import random
import time
from typing import Tuple, List, Generator

class StockDataSet:
    def __init__(self,
                 stock_sym: str,
                 input_size: int = 1,
                 num_steps: int = 30,
                 test_ratio: float = 0.1,
                 normalized: bool = True,
                 close_price_only: bool = True,
                 seed: int = None):
        """
        Initializes the StockDataSet object.

        Parameters:
            stock_sym (str): Stock symbol to identify the data file.
            input_size (int): Number of input features.
            num_steps (int): Number of steps in the sequence.
            test_ratio (float): Ratio of the dataset to be used for testing.
            normalized (bool): Whether to normalize the data.
            close_price_only (bool): Whether to use only the close price or both open and close prices.
            seed (int): Seed for random operations to ensure reproducibility.
        """
        self.stock_sym = stock_sym
        self.input_size = input_size
        self.num_steps = num_steps
        self.test_ratio = test_ratio
        self.close_price_only = close_price_only
        self.normalized = normalized

        if seed is not None:
            random.seed(seed)
        else:
            random.seed(time.time())

        raw_df = pd.read_csv(os.path.join("data", f"{stock_sym}.csv"))

        if close_price_only:
            self.raw_seq = raw_df['Close'].values
        else:
            self.raw_seq = raw_df[['Open', 'Close']].values.flatten()

        self.raw_seq = np.array(self.raw_seq)
        self.train_X, self.train_y, self.test_X, self.test_y = self._prepare_data(self.raw_seq)

    def info(self) -> str:
        """
        Returns the information about the dataset.

        Returns:
            str: Information about the dataset.
        """
        return f"StockDataSet [{self.stock_sym}] train: {len(self.train_X)} test: {len(self.test_y)}"

    def _prepare_data(self, seq: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepares the data for training and testing.

        Parameters:
            seq (np.ndarray): Sequence of stock prices.

        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Training and testing data.
        """
        seq = [seq[i * self.input_size: (i + 1) * self.input_size] for i in range(len(seq) // self.input_size)]

        if self.normalized:
            seq = [(seq[0] / seq[0][0] - 1.0)] + [(curr / seq[i][-1] - 1.0) for i, curr in enumerate(seq[1:])]

        X = np.array([seq[i: i + self.num_steps] for i in range(len(seq) - self.num_steps)])
        y = np.array([seq[i + self.num_steps] for i in range(len(seq) - self.num_steps)])

        train_size = int(len(X) * (1.0 - self.test_ratio))
        train_X, test_X = X[:train_size], X[train_size:]
        train_y, test_y = y[:train_size], y[train_size:]

        return train_X, train_y, test_X, test_y

    def generate_one_epoch(self, batch_size: int) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        Generates one epoch of training data.

        Parameters:
            batch_size (int): Size of each batch.

        Yields:
            Generator[Tuple[np.ndarray, np.ndarray], None, None]: Batches of training data.
        """
        num_batches = len(self.train_X) // batch_size
        if batch_size * num_batches < len(self.train_X):
            num_batches += 1

        batch_indices = list(range(num_batches))
        random.shuffle(batch_indices)
        for j in batch_indices:
            batch_X = self.train_X[j * batch_size: (j + 1) * batch_size]
            batch_y = self.train_y[j * batch_size: (j + 1) * batch_size]
            assert all(len(x) == self.num_steps for x in batch_X), "Inconsistent batch sizes."
            yield batch_X, batch_y

# Example usage
# dataset = StockDataSet('AAPL', input_size=1, num_steps=30, test_ratio=0.1, normalized=True, close_price_only=True, seed=42)
# print(dataset.info())
# for batch_X, batch_y in dataset.generate_one_epoch(batch_size=32):
#     print(batch_X, batch_y)
