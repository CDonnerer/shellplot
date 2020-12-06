# -*- coding: utf-8 -*-

import pytest
import numpy as np


from shellplot.plots import _plot, _hist


def test_plot():

    x = np.arange(-3, 3, 0.01)
    y = np.cos(x) ** 2
    _plot(x, y)


def test_hist():

    x = np.random.randn(100000)

    _hist(x, bins=20)
