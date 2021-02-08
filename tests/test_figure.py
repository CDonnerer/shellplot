"""Test figure api for shellplot
"""
import pytest

import numpy as np

from shellplot.figure import array_split, figure


@pytest.mark.parametrize(
    "x, y, expected_xy",
    [
        (
            np.array([[0, 1], [1, 0]]),
            np.array([[1, 1], [2, 2]]),
            [
                (np.array([0, 1]), np.array([1, 1])),
                (np.array([1, 0]), np.array([2, 2])),
            ],
        ),
    ],
)
def test_array_split_arrays(x, y, expected_xy):
    kwargs = {}

    for x, y, kwargs in array_split(x, y, kwargs):
        expected_x, expected_y = expected_xy.pop(0)
        np.testing.assert_array_equal(x, expected_x)
        np.testing.assert_array_equal(y, expected_y)


@pytest.mark.parametrize(
    # fmt: off
    "kwargs, expected_kwargs",
    [
        (
            {"label": ["a", "b"]},
            [{"label": "a"}, {"label": "b"}]
        ),
        (
            {"label": ["a"]},
            [{"label": "a"}, {}]
        ),
        (
            {},
            [{}, {}]
        ),
    ],
)
def test_array_split_label_kwargs(kwargs, expected_kwargs):
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[1, 1], [2, 2]])

    for x, y, kwargs in array_split(x, y, kwargs):
        assert kwargs == expected_kwargs.pop(0)


def test_figure_setters():
    """Faux test for checking that setters do not fail"""
    fig = figure()

    properties = {
        "xlim": (0, 1),
        "ylim": (0, 1),
        "xlabel": "a",
        "ylabel": "b",
        "xticks": [0, 1],
        "yticks": [0, 1],
        "xticklabels": ["a", "b"],
        "yticklabels": ["a", "b"],
    }
    for key, val in properties.items():
        getattr(fig, f"set_{key}")(val)
