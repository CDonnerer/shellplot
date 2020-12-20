# -*- coding: utf-8 -*-

import numpy as np

from shellplot.plots import _barh, _hist, _plot


def test_plot():
    x = np.arange(-3, 3, 0.01)
    y = np.cos(x) ** 2
    plt_str = _plot(x, y)
    assert isinstance(plt_str, str)


def test_scatter():
    x = np.arange(0, 100, 1)
    y = np.random.randn(100)
    color = np.array(["one"] * 70 + ["two"] * 30)
    plt_str = _plot(x, y, color=color)
    assert isinstance(plt_str, str)


def test_scatter():
    x = np.arange(0, 100, 1)
    y = np.random.randn(100)
    color = np.array(["one"] * 70 + ["two"] * 30)
    _plot(x, y, color=color)


def test_hist():
    x = np.random.randn(1000)
    plt_str = _hist(x, bins=20)
    assert isinstance(plt_str, str)


def test_barh():
    x = np.array([10, 56, 121, 67])
    labels = np.array(["one", "two", "three", "four"])
    plt_str = _barh(x, labels=labels)
    assert isinstance(plt_str, str)
