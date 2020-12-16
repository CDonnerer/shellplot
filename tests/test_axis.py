"""Testing axis class
"""
import pytest

import numpy as np

from shellplot.axis import Axis

np.random.seed(42)


@pytest.mark.parametrize(
    # fmt: off
    "x,expected_limits",
    [
        (np.random.uniform(1, 9, 300), (1, 9)),
        (np.random.uniform(1.02, 8.9, 300), (1, 9)),
        (np.random.uniform(-0.05, -0.01, 300), (-0.1, -0.01)),
        (np.random.uniform(-10.05, 2.36, 300), (-10.0, 2.4))
    ],
)
def test_axis_auto_limits(x, expected_limits):
    """Check whether automatically determined limits are sensible"""
    axis = Axis(display_length=80)
    axis = axis.fit(x)

    assert axis.limits == expected_limits


@pytest.mark.parametrize(
    # fmt: off
    "x,expected_display_x",
    [
        (np.array([0, 100]), np.array([0, 79])),
        (np.array([0, 50]), np.array([0, 40])),
        (np.array([0, 25]), np.array([0, 20])),
    ],
)
def test_axis_transform(x, expected_display_x):
    """"""
    axis = Axis(display_length=80)
    axis.limits = (0, 100)
    display_x = axis.fit_transform(x)

    np.testing.assert_array_equal(display_x, expected_display_x)
