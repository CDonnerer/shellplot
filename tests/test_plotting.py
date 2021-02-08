"""Tests for private plotting functions
"""
import pytest

import numpy as np

from shellplot._plotting import _add_hbar, _add_vbar

# -----------------------------------------------------------------------------
# Test canvas elements
# -----------------------------------------------------------------------------


@pytest.fixture
def expected_canvas_vbar():
    return np.array(
        [
            [0, 0, 0, 0, 0],
            [20, 20, 20, 0, 0],
            [0, 0, 0, 22, 0],
            [20, 20, 20, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )


def test_add_vbar(expected_canvas_vbar):
    canvas = np.zeros(shape=(5, 5), dtype=int)
    canvas = _add_vbar(canvas, start=1, width=1, height=3)
    np.testing.assert_equal(canvas, expected_canvas_vbar)


@pytest.fixture
def expected_canvas_hbar():
    return np.array(
        [
            [22, 0, 0, 22, 0],
            [22, 0, 0, 22, 0],
            [0, 20, 20, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )


def test_add_hbar(expected_canvas_hbar):
    canvas = np.zeros(shape=(5, 5), dtype=int)
    canvas = _add_hbar(canvas, start=0, width=2, height=2)
    np.testing.assert_equal(canvas, expected_canvas_hbar)
