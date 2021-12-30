"""Module that contains Axis class (usable for both x and y axis)

The main function of an axis is to transform from the data coordinates to the
display coordinates, hence we loosely follow an sklearn transformer api.

It can be used like so:

x_axis = Axis(display_length)
x_axis = x_axis.fit(x)
x_display = x_axis.transform(x)

where x_display is the data in display coordinates
"""
import numpy as np

from shellplot.utils import (
    difference_round,
    numpy_1d,
    round_down,
    round_up,
    timedelta_round,
    to_datetime,
    to_numeric,
    tolerance_round,
)


class Axis:
    def __init__(
        self,
        display_length: int = 20,
        label: str = None,
        limits=None,
        ticklabels=None,
        ticks=None,
        **kwargs
    ):
        self._is_datetime = False  # whether or not we are a datetime axis
        self._scale = None
        self._nticks = None

        self.display_max = display_length - 1
        self.label = label
        self.limits = limits
        self.ticks = ticks
        self.ticklabels = ticklabels

    # -------------------------------------------------------------------------
    # Properties that can be set / modified by the user
    # -------------------------------------------------------------------------

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def limits(self):
        return self._limits

    @limits.setter
    def limits(self, limits):
        self._limits = limits
        if limits is not None:
            self._limits, _ = to_numeric(np.array(limits))
            self._set_scale()
            self.ticks = self._auto_ticks()

    @property
    def nticks(self):
        if self._nticks is None:
            self._nticks = self._auto_nticks()
        return self._nticks

    @property
    def ticks(self):
        if self._ticks is None:
            self.ticks = self._auto_ticks()
        return self._ticks

    @ticks.setter
    def ticks(self, ticks):
        self._ticks = numpy_1d(ticks)
        self.ticklabels = ticks

    @property
    def ticklabels(self):
        return self._ticklabels

    @ticklabels.setter
    def ticklabels(self, labels):
        if labels is not None:
            if len(labels) != len(self.ticks):
                raise ValueError("Len of tick labels must equal len of ticks!")
            if self._is_datetime:
                labels = np.datetime_as_string(labels)
        self._ticklabels = numpy_1d(labels)

    # -------------------------------------------------------------------------
    # Fit & transform
    # -------------------------------------------------------------------------

    def fit(self, x):
        """Fit axis to get conversion from data to plot scale"""
        x, self._is_datetime = to_numeric(x)

        if self.limits is None:
            self.limits = self._auto_limits(x)
        if self.ticks is None:
            self.ticks = self._auto_ticks()

        self._set_scale()

        return self

    def transform(self, x):
        x, _ = to_numeric(x)
        x_scaled = self._scale * (x - self.limits[0]).astype(float)
        x_display = np.around(x_scaled).astype(int)
        return np.ma.masked_outside(x_display, 0, self.display_max)

    def fit_transform(self, x):
        self = self.fit(x)
        return self.transform(x)

    def gen_tick_labels(self):
        """Generate display tick location and labels"""
        display_ticks = self.transform(self.ticks)
        within_display = np.logical_and(
            display_ticks >= 0, display_ticks <= self.display_max
        )
        display_labels = self.ticklabels[within_display]
        display_ticks = display_ticks[within_display]

        return zip(display_ticks, display_labels)

    # -------------------------------------------------------------------------
    # Auto scaling & ticks
    # -------------------------------------------------------------------------

    def _set_scale(self):
        self._scale = self.display_max / float(self.limits[1] - self.limits[0])

    def _auto_limits(self, x, margin=0.25):
        """Automatically find reasonable axis limits"""
        x_max, x_min = x.max(), x.min()

        max_difference = margin * (x_max - x_min)
        ax_min = difference_round(x_min, round_down, max_difference)
        ax_max = difference_round(x_max, round_up, max_difference)

        return ax_min, ax_max

    def _auto_nticks(self):
        """Automatically find reasonable number of ticks that fit display"""
        max_ticks = int(1.5 * self.display_max ** 0.3) + 1
        ticks = np.arange(max_ticks, max_ticks - 2, -1)
        remainders = np.remainder(self.display_max, ticks)
        return ticks[np.argmin(remainders)] + 1

    def _auto_ticks(self):
        if not self._is_datetime:
            return self._auto_numeric_ticks()
        else:
            return self._auto_datetime_ticks()

    def _auto_numeric_ticks(self, tol=0.05):
        step, precision = tolerance_round(
            (self.limits[1] - self.limits[0]) / (self.nticks - 1),
            tol=tol,
        )
        return np.around(
            np.arange(self.limits[0], self.limits[1] + step, step), precision
        )

    def _auto_datetime_ticks(self):
        axis_td = to_datetime(np.array(self.limits, dtype="timedelta64[ns]"))
        limits_delta = axis_td[1] - axis_td[0]
        unit = timedelta_round(limits_delta)
        n_units = limits_delta / np.timedelta64(1, unit)
        td_step = np.timedelta64(int(n_units / (self.nticks - 1)), unit)

        return np.arange(
            np.datetime64(axis_td[0], unit),
            np.datetime64(axis_td[1], unit) + td_step,
            td_step,
        )
