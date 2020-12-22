"""Module that contains Axis class (usable for both x and y axis)

The main function of an axis is to transform from the data coordinates to the
display coordinates, hence we loosely follow an sklearn transfomer api.

It can be used like so:

x_axis = Axis(display_length)
x_axis = x_axis.fit(x)
x_display = x_axis.transform(x)

where x_display is the data in display coordinates

"""
import numpy as np

from shellplot.utils import round_down, round_up, tolerance_round


class Axis:
    def __init__(self, display_length, title=None, limits=None):
        self.display_max = display_length - 1
        self._title = title
        self._limits = limits

    # -------------------------------------------------------------------------
    # Public properties that can be set by the user
    # -------------------------------------------------------------------------

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
        self.fit()  # setting axis limits automatically fits the axis

    @property
    def n_ticks(self):
        if not hasattr(self, "_n_ticks"):
            self.n_ticks = int(self.display_max ** 0.3) + 2
        return self._n_ticks

    @n_ticks.setter
    def n_ticks(self, n_ticks):
        self._n_ticks = n_ticks

    @property
    def ticks(self):
        if not hasattr(self, "_ticks"):
            self.ticks = self._get_ticks()
        return self._ticks

    @ticks.setter
    def ticks(self, ticks):
        self._ticks = ticks

    @property
    def labels(self):
        if not hasattr(self, "_labels"):
            self.labels = self.ticks
        return self._labels

    @labels.setter
    def labels(self, labels):
        if len(labels) != len(self.ticks):
            raise ValueError("Len of tick labels must equal len of ticks!")
        self._labels = labels

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def fit(self, x=None):
        """Fit axis to get conversion from data to plot scale"""
        if self.limits is None:
            self.limits = self._auto_limits(x)

        self.scale = float(self.display_max) / (self.limits[1] - self.limits[0])
        return self

    def transform(self, x):
        return np.around(self.scale * (x - self.limits[0])).astype(int)

    def fit_transform(self, x):
        self = self.fit(x)
        return self.transform(x)

    def tick_labels(self):
        """Generate display tick location and labels"""
        display_ticks = self.transform(self.ticks)
        within_display = np.logical_and(
            display_ticks >= 0, display_ticks <= self.display_max
        )
        display_labels = self.labels[within_display]
        display_ticks = display_ticks[within_display]

        return list(zip(display_ticks, display_labels))  # generator?

    def _get_ticks(self):
        """"""
        step, precision = tolerance_round(
            (self.limits[1] - self.limits[0]) / self.n_ticks, tol=1e-1
        )
        return np.around(
            np.arange(self.limits[0], self.limits[1] + step, step), precision
        )

    def _auto_limits(self, x, frac=0.05):
        """Automatically find `good` axis limits"""

        x_max = x.max()
        x_min = x.min()

        max_difference = frac * (x_max - x_min)
        ax_min = self._difference_round(x_min, round_down, max_difference)
        ax_max = self._difference_round(x_max, round_up, max_difference)

        return ax_min, ax_max

    def _difference_round(self, val, round_func, max_difference):
        for dec in range(10):
            rounded = round_func(val, dec)
            if abs(rounded - val) <= max_difference:
                return rounded
