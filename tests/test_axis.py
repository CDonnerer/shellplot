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
        (np.random.uniform(1, 9, 100), (1, 9)),
        (np.random.uniform(1.02, 8.9, 100), (1, 9)),
        (np.random.uniform(-0.05, -0.01, 100), (-0.05, -0.01)),
        (np.array([-10.054, 2.36]), (-10.1, 2.4)),
        (np.array([0.000432424, 0.998]), (0, 1.0)),
        (np.array([0.00431, 0.00821]), (0.0043, 0.0083)),
        (np.array([172.1, 231.9]), (172, 232)),
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
    """Test axis transform from plot to display coordinates"""
    axis = Axis(display_length=80)
    axis.limits = (0, 100)
    display_x = axis.fit_transform(x)

    np.testing.assert_array_equal(display_x, expected_display_x)


@pytest.mark.parametrize(
    # fmt: off
    "limits,n_ticks,expected_ticks",
    [
        ((0, 1), 5, np.array([0, 0.2, 0.4, 0.6, 0.8, 1.0])),
        ((1, 9), 5, np.array([1, 3, 5, 7, 9])),
    ],
)
def test_axis_ticks(limits, n_ticks, expected_ticks):
    """Test axis ticks generation"""
    axis = Axis(display_length=80)
    axis.limits = limits
    axis.n_ticks = n_ticks
    ticks = axis._get_ticks()

    np.testing.assert_array_equal(ticks, expected_ticks)


@pytest.mark.parametrize(
    # fmt: off
    "limits,ticks,expected_tick_labels",
    [
        ((0, 1), np.array([0, 0.5, 1.0]), [(0, 0.0), (40, 0.5), (79, 1.0)]),
        ((0, 1), np.array([0.5, 1.5, 2]), [(40, 0.5)]),
        ((10, 12), np.array([10, 11, 12]), [(0, 10), (40, 11), (79, 12)]),
    ],
)
def test_axis_tick_labels(limits, ticks, expected_tick_labels):
    """Test axis ticks generation"""
    axis = Axis(display_length=80)
    axis.limits = limits
    axis.ticks = ticks
    tick_labels = axis.tick_labels()

    assert tick_labels == expected_tick_labels


@pytest.mark.parametrize(
    # fmt: off
    "ticks,labels",
    [
        (np.array([0, 0.5, 1.0]), np.array([0, 0.5, 1.0, 2.0])),
        (np.array([0.5, 1.5]), np.array(["a"])),
    ],
)
def test_axis_labels_len_error(ticks, labels):
    """Test error raising when tick labels do not match ticks"""
    axis = Axis(display_length=80)
    axis.ticks = ticks

    with pytest.raises(ValueError):
        axis.labels = labels


def test_axis_properties():
    """Faux test for property setting"""
    axis = Axis(display_length=80)
    axis.title = "title"
    axis.limits = (1, 9)
    axis.ticks = np.array([1, 3, 5, 7, 9])
    axis.labels = np.array(["a", "b", "c", "d", "e"])
