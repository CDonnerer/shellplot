# -*- coding: utf-8 -*-

import pytest

import numpy as np

from shellplot.plots import _add_hbar, _add_vbar, _barh, _boxplot, _hist, _plot

# -----------------------------------------------------------------------------
# 'Integration' style 'tests' that only check everything runs end to end
# -----------------------------------------------------------------------------


def test_plot():
    x = np.arange(-3, 3, 0.01)
    y = np.cos(x) ** 2
    plt_str = _plot(x, y)
    assert isinstance(plt_str, str)


def test_hist():
    x = np.random.randn(1000)
    plt_str = _hist(x, bins=20)
    assert isinstance(plt_str, str)


def test_barh():
    x = np.array([10, 56, 121, 67])
    labels = np.array(["one", "two", "three", "four"])
    plt_str = _barh(x, labels=labels)
    assert isinstance(plt_str, str)


def test_boxplot():
    x = np.random.randn(1000)
    plt_str = _boxplot(x)
    assert isinstance(plt_str, str)


# -----------------------------------------------------------------------------
# Unit tests
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
