"""Testing axis class
"""
import pytest

import numpy as np

from shellplot.axis import Axis


@pytest.fixture(autouse=True)
def set_np_seed():
    np.random.seed(42)


@pytest.mark.parametrize(
    # fmt: off
    "x,expected_limits",
    [
        (np.random.uniform(1, 9, 100), np.array([1, 9])),
        (np.random.uniform(1.02, 8.9, 100), np.array([1, 9])),
        (np.random.uniform(-0.05, -0.01, 100), np.array([-0.05, -0.01])),
        (np.array([-10.054, 2.36]), np.array([-11, 3])),
        (np.array([0.000432424, 0.998]), np.array([0, 1])),
        (np.array([0.00431, 0.00821]), np.array([0.004, 0.009])),
        (np.array([172.1, 231.9]), np.array([172, 232])),
    ],
)
def test_axis_auto_limits(x, expected_limits):
    """Check whether automatically determined limits are sensible"""
    axis = Axis(display_length=81)
    axis = axis.fit(x)
    np.testing.assert_array_equal(axis.limits, expected_limits)


@pytest.mark.parametrize(
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
    "axis, expected_n_ticks",
    [
        (Axis(display_length=20), 4),
        (Axis(display_length=30), 5),
        (Axis(display_length=50), 5),
        (Axis(display_length=80), 7),
    ],
)
def test_axis_auto_nticks(axis, expected_n_ticks):
    """Auto n_ticks test"""
    n_ticks = axis._auto_nticks()
    assert n_ticks == expected_n_ticks


@pytest.mark.parametrize(
    # fmt: off
    "limits, n_ticks, expected_ticks",
    [
        ((0, 1), 5, np.array([0, 0.25, 0.5, 0.75, 1.0])),
        ((1, 9), 5, np.array([1, 3, 5, 7, 9])),
    ],
)
def test_axis_ticks(limits, n_ticks, expected_ticks):
    """Test axis ticks generation"""
    axis = Axis(display_length=80)
    axis.limits = limits
    axis.nticks = n_ticks

    np.testing.assert_array_equal(axis.ticks, expected_ticks)


@pytest.mark.parametrize(
    "limits, n_ticks, expected_labels",
    [
        (
            (np.datetime64("2001-01-01"), np.datetime64("2001-01-03")),
            3,
            np.array(["2001-01-01", "2001-01-02", "2001-01-03"]),
        ),
    ],
)
def test_axis_datetime_ticks(limits, n_ticks, expected_labels):
    axis = Axis(display_length=79)
    axis.nticks = n_ticks
    axis.fit(np.array(limits))
    ticklabels = axis.ticklabels

    assert list(ticklabels) == list(expected_labels)


@pytest.mark.parametrize(
    # fmt: off
    "limits,ticks,expected_tick_labels",
    [
        ((0, 1), np.array([0, 0.5, 1.0]), [(0, 0.0), (40, 0.5), (79, 1.0)]),
        ((0, 1), np.array([0.5, 1.5, 2]), [(40, 0.5)]),
        ((10, 12), np.array([10, 11, 12]), [(0, 10), (40, 11), (79, 12)]),
    ],
)
def test_axis_display_ticks(limits, ticks, expected_tick_labels):
    """Test axis ticks generation"""
    axis = Axis(display_length=80)
    axis.limits = limits
    axis.ticks = ticks
    tick_labels = list(axis.generate_display_ticks())

    assert tick_labels == expected_tick_labels


@pytest.mark.parametrize(
    # fmt: off
    "ticks,labels",
    [
        (np.array([0, 0.5, 1.0]), np.array([0, 0.5, 1.0, 2.0])),
        (np.array([0.5, 1.5]), np.array(["a"])),
    ],
)
def test_axis_ticklabels_len_error(ticks, labels):
    """Test error raising when tick labels do not match ticks"""
    axis = Axis(display_length=80)
    axis.ticks = ticks

    with pytest.raises(ValueError):
        axis.ticklabels = labels


# -----------------------------------------------------------------------------
# Test axis property setting
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    # fmt: off
    "axis_property, value, expected_value",
    [
        ("label", "my fun label", "my fun label"),
        ("limits", (4, 5), np.array([4, 5])),
        ("nticks", 5, 5),
        ("ticks", (0, 1, 2), np.array([0, 1, 2])),
        ("ticklabels", ("a", "b", "c"), np.array(["a", "b", "c"])),
        (
            "ticklabels",
            (
                np.datetime64("2001-01-01"),
                np.datetime64("2001-01-03"),
                np.datetime64("2001-01-05"),
            ),
            np.array(["2001-01-01", "2001-01-03", "2001-01-05"])
        )
    ],
)
def test_axis_property_setting(axis_property, value, expected_value):
    axis = Axis()
    axis = axis.fit((0, 1))
    axis.nticks = 3

    setattr(axis, axis_property, value)
    set_value = getattr(axis, axis_property)

    if isinstance(expected_value, np.ndarray):
        np.testing.assert_array_equal(set_value, expected_value)
    else:
        assert set_value == expected_value


def test_axis_limit_update_changes_ticks():
    """Check that updating limits leads to new axis ticks"""
    axis = Axis(display_length=80)

    axis.limits = (0, 300)
    np.testing.assert_array_equal(
        axis.ticks, np.array([0, 50, 100, 150, 200, 250, 300])
    )

    axis.limits = (50, 80)
    np.testing.assert_array_equal(axis.ticks, np.array([50, 55, 60, 65, 70, 75, 80]))


def test_axis_properties():
    """Faux test for property setting"""
    axis = Axis(display_length=80)
    axis.title = "title"
    axis.limits = (1, 9)
    axis.ticks = np.array([1, 3, 5, 7, 9])
    axis.labels = np.array(["a", "b", "c", "d", "e"])
