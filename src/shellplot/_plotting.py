"""Private plotting functionality.

These functions require an instantiated figure, their call then updates the
figure state.
"""

import numpy as np

from shellplot.drawing import LINES, MARKERS
from shellplot.utils import numpy_1d, numpy_2d


def _plot(fig, x, y, l_kwargs):
    """Scatterplot"""

    fig.x_axis.fit(np.concatenate([x for x in x]))
    fig.y_axis.fit(np.concatenate([y for y in y]))

    for x, y, plt_kwargs in zip(x, y, l_kwargs):
        _single_plot(
            fig=fig,
            x=x,
            y=y,
            marker=plt_kwargs.get("marker", next(MARKERS)),
            line=plt_kwargs.get("line", next(LINES)),
            label=plt_kwargs.get("label"),
        )


def _single_plot(fig, x, y, marker=None, line=None, label=None):
    x_scaled = fig.x_axis.transform(numpy_1d(x))
    y_scaled = fig.y_axis.transform(numpy_1d(y))

    idx, idy = _within_display(x_scaled, y_scaled)

    _add_xy(
        canvas=fig.canvas,
        idx=idx,
        idy=idy,
        marker=marker,
        line=line,
    )

    if label is not None:
        key = marker or line
        fig.legend.update({key: label})


def _within_display(x, y):
    outside_display = np.logical_or(x.mask, y.mask)
    x.mask = outside_display
    y.mask = outside_display

    idx = x.compressed()
    idy = y.compressed()
    return idx, idy


def _hist(fig, x, bins=10, **kwargs):
    """Histogram"""
    _check_bins(bins, fig.x_axis)

    x = numpy_1d(x)
    x = x[~np.isnan(x)]
    counts, bin_edges = np.histogram(x, bins)

    fig.y_axis.limits = (0, max(counts))
    counts_scaled = fig.y_axis.transform(counts)
    fig.x_axis.fit(bin_edges)

    bin = 0
    bin_width = fig.x_axis.display_max // len(counts) - 1

    for count in counts_scaled:
        _add_vbar(fig.canvas, bin, bin_width, count)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(counts)
    fig.x_axis.scale = display_max / (fig.x_axis.limits[1] - fig.x_axis.limits[0])


def _check_bins(bins, x_axis):
    if isinstance(bins, int):
        bin_len = bins
    elif isinstance(bins, np.ndarray) or isinstance(bins, list):
        bin_len = len(bins)
    else:
        raise ValueError("Please provider either integer or array of bins!")
    if bin_len > x_axis.display_max:
        raise ValueError("Number of bins needs to be less than figsize along x!")


def _barh(fig, x, labels=None, **kwargs):
    """Horizontal bar plot"""

    fig.x_axis.limits = (0, x.max())
    x_scaled = fig.x_axis.fit_transform(x)

    fig.y_axis.fit(np.arange(0, len(x) + 1, 1))
    fig.y_axis.ticks = np.array(list(range(len(x)))) + 0.5

    if labels is not None:
        fig.y_axis.ticklabels = labels

    bin = 0
    bin_width = fig.y_axis.display_max // len(x) - 1

    for val in x_scaled.data:
        _add_hbar(fig.canvas, bin, bin_width, val)
        bin += bin_width + 1

    display_max = (bin_width + 1) * len(x)
    fig.y_axis.scale = (display_max) / (fig.y_axis.limits[1] - fig.y_axis.limits[0])


def _boxplot(fig, x, labels=None, **kwargs):
    """Box plot"""

    x = numpy_2d(x)
    x = np.ma.masked_where(np.isnan(x), x)

    quantiles = np.array(
        [np.quantile(dist[dist.mask == 0], q=[0, 0.25, 0.5, 0.75, 1.0]) for dist in x]
    )
    quantiles_scaled = fig.x_axis.fit_transform(quantiles)

    fig.y_axis.fit(np.array([0, len(x)]))
    y_lims = fig.y_axis.transform(
        np.array([0.2, 0.50, 0.8]) + np.arange(0, len(x), 1)[np.newaxis].T
    )
    fig.y_axis.ticks = np.arange(0.5, len(x), 1)

    if labels is not None:
        fig.y_axis.ticklabels = numpy_1d(labels)

    for ii in range(len(x)):
        quants = quantiles_scaled[ii, :]
        lims = y_lims[ii, :]
        _add_box_and_whiskers(fig.canvas, quants, lims)


# -----------------------------------------------------------------------------
# Function to add canvas elements
# -----------------------------------------------------------------------------


def _add_xy(canvas, idx, idy, marker=None, line=None):
    """Add x, y series to canvas, as marker and/ or line"""
    if line is not None:
        x_line, y_line = _line_interp(idx, idy)
        canvas[x_line, y_line] = line
    if marker is not None:
        canvas[idx, idy] = marker
    return canvas


def _line_interp(x, y, round_tol=0.4):
    """Interpolate for line plotting"""
    x_interp = np.arange(x.min(), x.max(), 1)
    y_interp = np.interp(x_interp, x, y)

    # Point selection is turned off for now
    # is_discrete = np.isclose(
    #     y_interp,
    #     np.around(y_interp).astype(int),
    #     atol=round_tol,
    # )
    is_discrete = True

    x_line = x_interp[is_discrete].astype(int)
    y_line = np.around(y_interp[is_discrete]).astype(int)

    return x_line, y_line


def _add_vbar(canvas, start, width, height):
    """Add a vertical bar to the canvas"""
    canvas[start, :height] = 20
    canvas[start + 1 : start + 1 + width, height] = 22
    canvas[start + 1 + width, :height] = 20
    return canvas


def _add_hbar(canvas, start, width, height):
    """Add a horizontal bar to the canvas"""
    canvas[:height, start] = 22
    canvas[height, start + 1 : start + 1 + width] = 20
    canvas[:height, start + 1 + width] = 22
    return canvas


def _add_box_and_whiskers(canvas, quantiles, limits):
    """Add a box and whiskers to the canvas"""
    for jj in range(5):
        canvas[quantiles[jj], limits[0] + 1 : limits[2]] = 20

    canvas[quantiles[0] + 1 : quantiles[1], limits[1]] = 22
    canvas[quantiles[3] + 1 : quantiles[4], limits[1]] = 22

    canvas[quantiles[1] + 1 : quantiles[3], limits[2]] = 22
    canvas[quantiles[1] + 1 : quantiles[3], limits[0]] = 22
    return canvas
