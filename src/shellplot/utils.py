"""Utility functions
"""
import math
import os
from functools import singledispatch

import numpy as np
import pandas as pd

__all__ = ["load_dataset"]

ANCHOR_DATETIME = np.datetime64("1970-01-01")  # I remember the day well


def load_dataset(name: str) -> pd.DataFrame:
    """Load dataset from shellplot library

    Parameters
    ----------
    name : str
        Name of the dataset. Currently, available options are:
            - `penguins`

    Returns
    -------
    pd.DataFrame
        Pandas dataframe of dataset

    """
    module_path = os.path.dirname(__file__)
    dataset_path = os.path.join(module_path, "datasets", f"{name}.csv")

    return pd.read_csv(dataset_path)


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
    return _round_to_decimals(n=n, decimals=decimals, round_func=math.ceil)


def round_down(n, decimals=0):
    return _round_to_decimals(n=n, decimals=decimals, round_func=math.floor)


def _round_to_decimals(n, decimals, round_func):
    if decimals == 0:  # avoid float div for int rounded value
        return round_func(n)
    else:
        multiplier = 10 ** decimals
        return round_func(n * multiplier) / multiplier


def timedelta_round(x):
    """Given a numpy timedelta, find the largest time unit without changing value"""
    units = ["Y", "M", "D", "h", "m", "s", "ms", "us", "ns"]
    for unit in units:
        x_rounded = x.astype(f"timedelta64[{unit}]")
        if x_rounded == x:  # TODO: apparently raises a # WARNING: ?
            return unit


def remove_any_nan(x, y):
    """Given two np.ndarray, remove indeces where any is nan"""
    is_any_nan = np.isnan(x) | np.isnan(y)
    return x[~is_any_nan], y[~is_any_nan]


@singledispatch
def numpy_2d(x):
    """Reshape and transform various array-like inputs to 2d np arrays"""


@numpy_2d.register
def _(x: np.ndarray):
    if len(x.shape) == 1:
        return x[np.newaxis]
    elif len(x.shape) == 2:
        return x
    else:
        raise ValueError("Array dimensions need to be <= 2!")


@numpy_2d.register
def _(x: pd.DataFrame):
    return x.to_numpy().transpose()


@numpy_2d.register(pd.Series)
@numpy_2d.register(pd.Index)
def _(x):
    return x.to_numpy()[np.newaxis]


@numpy_2d.register
def _(x: list):
    if isinstance(x[0], np.ndarray):
        return numpy_1d(x)
    elif isinstance(x[0], list):
        return np.array([numpy_1d(x) for x in x])
    else:
        return np.array([numpy_1d((x))])


@singledispatch
def numpy_1d(x):
    """Reshape and transform various array-like inputs to 1d np arrays"""


@numpy_1d.register(np.ndarray)
def _(x):
    return x


@numpy_1d.register(pd.Series)
@numpy_1d.register(pd.Index)
def _(x):
    return x.to_numpy()


@numpy_1d.register(pd.DataFrame)
def _(x):
    return x.to_numpy().squeeze()


@numpy_1d.register(list)
def _(x):
    return np.array(x)


@numpy_1d.register(str)
def _(x):  # TODO: this should be any non-iterable
    return np.array([x])


@singledispatch
def get_label(x):
    """Try to get names out of array-like inputs"""
    pass


@get_label.register(pd.DataFrame)
def _(x):
    return list(x)


@get_label.register(pd.Series)
def _(x):
    return x.name


@singledispatch
def get_index(x):
    """Try to get index out of array-like inputs"""


@get_index.register(pd.Series)
@get_index.register(pd.DataFrame)
def _(x):
    return np.array(x.index)


def to_numeric(x):
    x = numpy_1d(x)
    """Convert np array to numeric values"""
    if x.dtype.kind in np.typecodes["Datetime"]:
        return x.astype("datetime64[ns]") - ANCHOR_DATETIME, x.dtype
    else:
        return x, False


def to_datetime(x):
    return x + ANCHOR_DATETIME
