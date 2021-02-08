import pytest

import numpy as np
import pandas as pd

from shellplot.utils import (
    get_index,
    get_label,
    load_dataset,
    numpy_1d,
    numpy_2d,
    remove_any_nan,
    round_down,
    round_up,
    timedelta_round,
    tolerance_round,
)


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
    "number,decimals,expected",
    [
        (0.321, 2, 0.33),
        (1.214, 2, 1.22),
        (1.214, 1, 1.3),
        (1.214, 0, 2),
    ],
)
def test_round_up(number, decimals, expected):
    rounded = round_up(number, decimals)
    assert rounded == expected


@pytest.mark.parametrize(
    "number,decimals,expected",
    [
        (0.321, 2, 0.32),
        (1.814, 2, 1.81),
        (1.814, 1, 1.8),
        (1.814, 0, 1),
    ],
)
def test_round_down(number, decimals, expected):
    rounded = round_down(number, decimals)
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


@pytest.mark.parametrize(
    "x, expected_np_2d",
    [
        (np.array([0, 1]), np.array([[0, 1]])),
        (np.array([[0, 1]]), np.array([[0, 1]])),
        ([np.array([0, 1])], np.array([[0, 1]])),
        (pd.DataFrame(np.array([[0], [1]])), np.array([[0, 1]])),
        (pd.Series([0, 1]), np.array([[0, 1]])),
        ([0, 1], np.array([[0, 1]])),
        ([[0, 1], [0, 2]], np.array([[0, 1], [0, 2]])),
    ],
)
def test_numpy_2d(x, expected_np_2d):
    np_2d = numpy_2d(x)
    np.testing.assert_equal(np_2d, expected_np_2d)


@pytest.mark.parametrize(
    "x, expected_np_1d",
    [
        (np.array([0, 1]), np.array([0, 1])),
        (pd.Series(np.array([0, 1])), np.array([0, 1])),
        (pd.Index([0, 1]), np.array([0, 1])),
        (pd.DataFrame(np.array([0, 1])), np.array([0, 1])),
        ([0, 1], np.array([0, 1])),
        ("box", np.array(["box"])),
    ],
)
def test_numpy_1d(x, expected_np_1d):
    np_1d = numpy_1d(x)
    np.testing.assert_equal(np_1d, expected_np_1d)


@pytest.mark.parametrize(
    "x, expected_label",
    [
        (pd.Series(data=[0, 1], name="my_series"), "my_series"),
        # (pd.DataFrame({"feat_1": [0, 1], "feat_2": [0, 1]}), TODO
    ],
)
def test_get_label(x, expected_label):
    label = get_label(x)
    assert label == expected_label


@pytest.mark.parametrize(
    "x, expected_index",
    [
        (pd.Series(data=[0, 1], index=[1, 0]), np.array([1, 0])),
        (pd.DataFrame({"feat_1": [0, 1]}, index=[1, 0]), np.array([1, 0])),
        (np.array([1, 0]), None),
    ],
)
def test_get_index(x, expected_index):
    index = get_index(x)
    np.testing.assert_equal(index, expected_index)


@pytest.mark.parametrize(
    "x, expected_unit",
    [
        (np.timedelta64(86400000000000, "ns"), "D"),
        (np.timedelta64(3600000000000, "ns"), "h"),
        (np.timedelta64(1000000, "ns"), "ms"),
    ],
)
def test_timedelta_round(x, expected_unit):
    assert timedelta_round(x) == expected_unit
