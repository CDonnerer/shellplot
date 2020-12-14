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
