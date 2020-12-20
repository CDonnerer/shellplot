"""Shellplot plots
"""
import numpy as np
import pandas as pd

from shellplot.axis import Axis
from shellplot.drawing import draw
from shellplot.utils import remove_any_nan

DISPLAY_X = 70
DISPLAY_Y = 25


def plot(x, y, **kwargs):
    plt_str = _plot(x=x, y=y, **kwargs)
    print(plt_str)


def get_name(x):
    if isinstance(x, pd.Series):
        return x.name
    else:
        return None


def _plot(x, y, x_title=None, y_title=None, color=None):
    x, y = remove_any_nan(x, y)

    if x_title is None:
        x_title = get_name(x)
    if y_title is None:
        y_title = get_name(y)

    x_axis = Axis(DISPLAY_X, title=x_title)
    y_axis = Axis(DISPLAY_Y, title=y_title)

    x_scaled = x_axis.fit_transform(x)
    y_scaled = y_axis.fit_transform(y)

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y))

    if color is not None:
        values = np.unique(color)

        for ii, val in enumerate(values):
            mask = val == color
            canvas[x_scaled[mask], y_scaled[mask]] = ii + 1

        legend = {ii + 1: val for ii, val in enumerate(values)}
    else:
        canvas[x_scaled, y_scaled] = 1
        legend = None

    plt_str = draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis, legend=legend)
    return plt_str


def hist(x, bins=10, x_title=None, **kwargs):
    plt_str = _hist(x=x, bins=bins, x_title=x_title, **kwargs)
    print(plt_str)


def _hist(x, bins=10, x_title=None, **kwargs):
    x = x[~np.isnan(x)]

    counts, bin_edges = np.histogram(x, bins)

    y_axis = Axis(DISPLAY_Y, title="counts")
    x_axis = Axis(DISPLAY_X, title=x_title)

    counts_scaled = y_axis.fit_transform(counts)
    x_axis = x_axis.fit(bin_edges)

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y))

    bin = 0
    bin_width = int((DISPLAY_X - 1) / len(counts)) - 1

    for count in counts_scaled:
        canvas[bin, :count] = 20
        canvas[bin + 1 : bin + 1 + bin_width, count] = 21
        canvas[bin + 1 + bin_width, :count] = 20
        bin += bin_width + 1

    # this bit doesn't seem entirely right
    display_max = (bin_width + 1) * len(counts)
    x_axis.scale = (display_max + bin_width) / (x_axis.limits[1] - x_axis.limits[0])

    plt_str = draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)
    return plt_str


def barh(x, **kwargs):
    plt_str = _barh(x, **kwargs)
    print(plt_str)


def _barh(x, labels=None, x_title=None, y_title=None):
    y_axis = Axis(DISPLAY_Y, title=y_title)
    x_axis = Axis(DISPLAY_X, title=x_title)

    x_axis.limits = (0, int(1.01 * max(x)))
    x_scaled = x_axis.fit_transform(x)

    y_axis = y_axis.fit(list(range(len(x) + 1)))
    y_axis.ticks = np.array(list(range(len(x)))) + 0.5

    if labels is None:
        y_axis.labels = np.array(list(range(len(x))))
    else:
        y_axis.labels = labels

    canvas = np.zeros(shape=(DISPLAY_X, DISPLAY_Y))

    bin = 1
    bin_width = int((DISPLAY_Y - 1) / len(x)) - 1

    for val in x_scaled:
        canvas[:val, bin - 1] = 22
        canvas[val, bin : bin + bin_width] = 20
        canvas[val, bin + bin_width : bin + bin_width + 1] = 23
        canvas[:val, bin + bin_width] = 22
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(x)
    y_axis.scale = (display_max) / (y_axis.limits[1] - y_axis.limits[0])

    plt_str = draw(canvas=canvas, y_axis=y_axis, x_axis=x_axis)
    return plt_str
