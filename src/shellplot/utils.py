"""Utility functions
"""
import math
import os

import numpy as np
import pandas as pd


def tolerance_round(x, tol=1e-3):
    error = 1.0
    decimals = 0

    while error > tol:
        if decimals == 0:
            x_rounded = round(x)
        else:
            x_rounded = round(x, decimals)
        fudge = 1e-9  # protect against zero div
        error = (x - x_rounded) / (x + fudge)
        decimals += 1

    return x_rounded, decimals


def round_up(n, decimals=0):
    if decimals == 0:  # avoid float div for int rounded value
        return math.ceil(n)
    else:
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=0):
    if decimals == 0:  # avoid float div for int rounded value
        return math.floor(n)
    else:
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier


def remove_any_nan(x, y):
    """Given two np.ndarray, remove indeces where any is nan"""
    is_any_nan = np.isnan(x) | np.isnan(y)
    return x[~is_any_nan], y[~is_any_nan]


def load_dataset(name):
    module_path = os.path.dirname(__file__)
    dataset_path = os.path.join(module_path, "datasets", f"{name}.csv")

    return pd.read_csv(dataset_path)


def numpy_2d(x):
    """Reshape and transform various array-like inputs to 2d np arrays"""
    if isinstance(x, np.ndarray):
        if len(x.shape) == 1:
            return x[np.newaxis]
        else:
            return x
    elif isinstance(x, pd.DataFrame):
        return x.to_numpy().transpose()
    elif isinstance(x, list):
        return x
    else:
        return None
