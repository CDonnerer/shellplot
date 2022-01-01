"""Module that contains Axis class (usable for both x and y axis)
"""
from typing import Optional

import numpy as np

from shellplot.utils import (
    array_like,
    difference_round,
    is_datetime,
    numpy_1d,
    round_down,
    round_up,
    timedelta_round,
    to_datetime,
    to_numeric,
    tolerance_round,
)


class Axis:
    """Enables mapping from data to display / plot coordinates.

    We loosely follow the sklearn transformer api:

    >>> axis = Axis()
    >>> axis = x_axis.fit(x_data)
    >>> x_display = x_axis.transform(x_data)

    where `x_data` and `x_display` correspond to data and display coordinates,
    respectively.

    When calling `.fit`, we will automatically determine 'reasonable' axis
    limits and tick labels. Note that these can also be set by the user.
    """

    def __init__(
        self,
        display_length: int = 20,
        label: Optional[str] = None,
        limits: Optional[array_like] = None,
        ticklabels: Optional[array_like] = None,
        ticks: Optional[array_like] = None,
        nticks: Optional[int] = None,
    ):
        """Instantiate a new Axis.

        Parameters
        ----------
        display_length : int, optional
            Length of axis, in characters, default 20
        label : Optional[str], optional
            Axis label, default None
        limits : Optional[array_like], optional
            Axis limits, default None (auto-generated)
        ticklabels : Optional[array_like], optional
            Labels for axis ticks, default None (auto-generated, as ticks)
        ticks : Optional[array_like], optional
            Where the axis ticks should be, default None (auto-generated)
        nticks : Optional[int], optional
            Number of axis ticks, default None (auto-generated)
        """
        self.display_max = display_length - 1
        self._is_datetime = False  # whether or not we are a datetime axis
        self._scale = None

        self.label = label
        self.limits = limits
        self.nticks = nticks
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
        if limits is not None:  # new limits need to update scale and ticks
            self._limits = to_numeric(limits)
            self._set_scale()
            self._reset_ticks()

    @property
    def nticks(self):
        if self._nticks is None:
            self._nticks = self._auto_nticks()
        return self._nticks

    @nticks.setter
    def nticks(self, nticks):
        self._reset_ticks()
        self._nticks = nticks

    @property
    def ticks(self):
        if self._ticks is None:
            self._ticks = self._auto_ticks()
        return self._ticks

    @ticks.setter
    def ticks(self, ticks):
        self._reset_ticks()
        self._ticks = numpy_1d(ticks)

    @property
    def ticklabels(self):
        if self._ticklabels is None:
            self._ticklabels = self._auto_ticklabels()
        return self._ticklabels

    @ticklabels.setter
    def ticklabels(self, ticklabels):
        if ticklabels is not None:
            if len(ticklabels) != len(self.ticks):
                raise ValueError("Len of tick labels must equal len of ticks!")
            if is_datetime(ticklabels):
                ticklabels = np.datetime_as_string(ticklabels)
        self._ticklabels = numpy_1d(ticklabels)

    # -------------------------------------------------------------------------
    # Public methods: fit, transform and generate ticks
    # -------------------------------------------------------------------------

    def fit(self, x):
        """Fit axis to get conversion from data to plot scale"""
        self._is_datetime = is_datetime(x)
        x = to_numeric(x)

        if self.limits is None:
            self._limits = self._auto_limits(x)

        self._set_scale()
        return self

    def transform(self, x):
        """Transform data to the plot coordinates"""
        x = to_numeric(x)
        x_scaled = self._scale * (x - self.limits[0]).astype(float)
        x_display = np.around(x_scaled).astype(int)
        return np.ma.masked_outside(x_display, 0, self.display_max)

    def fit_transform(self, x):
        """Fit axis and transform data to the plot coordinates"""
        self = self.fit(x)
        return self.transform(x)

    def generate_display_ticks(self):
        """Generate display tick locations and labels"""
        display_ticks = self.transform(self.ticks)
        within_display = np.logical_and(
            display_ticks >= 0, display_ticks <= self.display_max
        )
        display_labels = self.ticklabels[within_display]
        display_ticks = display_ticks[within_display]

        return zip(display_ticks, display_labels)

    # -------------------------------------------------------------------------
    # Private methods: Auto scaling & ticks
    # -------------------------------------------------------------------------

    def _set_scale(self):
        self._scale = self.display_max / float(self.limits[1] - self.limits[0])

    def _auto_limits(self, x, margin=0.25):
        """Automatically find good axis limits"""
        x_max, x_min = x.max(), x.min()

        max_difference = margin * (x_max - x_min)
        ax_min = difference_round(x_min, round_down, max_difference)
        ax_max = difference_round(x_max, round_up, max_difference)

        return ax_min, ax_max

    def _auto_nticks(self):
        """Automatically find number of ticks that fit display"""
        max_ticks = int(1.5 * self.display_max ** 0.3) + 1
        ticks = np.arange(max_ticks, max_ticks - 2, -1)
        remainders = np.remainder(self.display_max, ticks)
        return ticks[np.argmin(remainders)] + 1

    def _auto_ticks(self):
        """Automatically find good axis ticks"""
        if self.limits is None:
            raise ValueError("Please fit axis or set limits first!")
        elif not self._is_datetime:
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
        )[: self.nticks]

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
        )[: self.nticks]

    def _auto_ticklabels(self):
        if self._is_datetime:
            return np.datetime_as_string(self.ticks)
        else:
            return self.ticks

    def _reset_ticks(self):
        self._ticks = None
        self._ticklabels = None
