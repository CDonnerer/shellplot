# -*- coding: utf-8 -*-

import numpy as np

from shellplot.plots import _hist, _plot


def test_plot():
    x = np.arange(-3, 3, 0.01)
    y = np.cos(x) ** 2
    _plot(x, y)


def test_hist():
    x = np.random.randn(1000)
    _hist(x, bins=20)
