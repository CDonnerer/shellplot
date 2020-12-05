# -*- coding: utf-8 -*-

import pytest
from shellplot.plots import plot, hist

__author__ = "Christian Donnerer"
__copyright__ = "Christian Donnerer"
__license__ = "mit"

def test_plot():
    import numpy as np

    x = np.arange(-3, 3, .01)
    y = np.cos(x)**2
    plot(x, y)


def test_hist():
    import numpy as np

    x = np.random.randn(100000)

    hist(x, bins=20)
