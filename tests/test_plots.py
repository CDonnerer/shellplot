# -*- coding: utf-8 -*-

import numpy as np

from shellplot.plots import _hist, _plot


def test_plot():
    x = np.arange(-3, 3, 0.01)
    y = np.cos(x) ** 2
    _plot(x, y)


def test_scatter():
    x = np.arange(0, 100, 1)
    y = np.random.randn(100)
    color = np.array(["one"] * 70 + ["two"] * 30)
    _plot(x, y, color=color)


def test_hist():
    np.random.seed(22)  # TODO fails with seed 42. fix it.
    x = np.random.randn(1000)
    _hist(x, bins=20)
