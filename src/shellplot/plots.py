"""Shellplot plots
"""
import numpy as np
import pandas as pd

from shellplot.drawing import draw
from shellplot.utils import remove_any_nan, tolerance_round

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


class Axis:
    def __init__(self, display_length, title=None, limits=None):
        self.display_length = display_length - 1
        self._title = title
        self._limits = limits

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, limits):
        self._limits = limits

    def fit(self, x):
        """Fit axis to get conversion from data to plot scale"""
        if self.limits is None:
            self.limits = self._determine_limits(x)

        self.scale = float(self.display_length) / (self.limits[1] - self.limits[0])
        return self

    def transform(self, x):
        return (self.scale * (x - self.limits[0])).astype(int)

    def fit_transform(self, x):
        self = self.fit(x)
        return self.transform(x)

    def ticks(self, n=5):
        """TODO. this functions is a mess"""
        step, precision = tolerance_round(
            (self.limits[1] - self.limits[0]) / n, tol=1e-1
        )

        labels = np.around(
            np.arange(self.limits[0], self.limits[1] + step, step), precision
        )
        ticks = self.transform(labels)

        if ticks[-1] > self.display_length:
            ticks = ticks[:-1]
            labels = labels[:-1]

        return list(zip(ticks, labels))

    def _determine_limits(self, x):
        plot_min = min(x)
        plot_max = max(x)
        rattle_factor = 0.03

        ax_min, _ = tolerance_round(
            plot_min - rattle_factor * np.sign(plot_min) * plot_min, tol=1e-1
        )
        ax_max, _ = tolerance_round(
            plot_max + rattle_factor * np.sign(plot_max) * plot_max, tol=1e-1
        )
        return ax_min, ax_max
