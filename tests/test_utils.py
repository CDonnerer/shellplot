import pytest

import numpy as np
import pandas as pd

from shellplot.utils import load_dataset, remove_any_nan, tolerance_round


@pytest.mark.parametrize(
    "number,expected",
    [
        (0, 0),
        (0.399997, 0.4),
        (102.1, 102),
        (1.499997, 1.5),
        (503.4, 503),
        (-0.32339, -0.3),
    ],
)
def test_tolerance_round(number, expected):
    rounded, _ = tolerance_round(number, tol=1e-1)

    assert rounded == expected


@pytest.mark.parametrize(
    "x, y, expected_x, expected_y",
    [
        (np.array([0, np.nan]), np.array([1, 2]), np.array([0]), np.array([1])),
        (np.array([0, 1]), np.array([np.nan, 2]), np.array([1]), np.array([2])),
        (np.array([0, np.nan]), np.array([1, np.nan]), np.array([0]), np.array([1])),
    ],
)
def test_remove_any_nan(x, y, expected_x, expected_y):
    no_nan_x, no_nan_y = remove_any_nan(x, y)

    np.testing.assert_equal(no_nan_x, expected_x)
    np.testing.assert_equal(no_nan_y, expected_y)


@pytest.mark.parametrize(
    "name",
    [("penguins")],
)
def test_load_dataset(name):
    df = load_dataset(name)
    assert isinstance(df, pd.DataFrame)
