"""API for pandas plotting backend
"""

import shellplot.plots as plt


def plot(data, kind, **kwargs):
    # TODO: check kind

    x_col = kwargs.get("x")
    y_col = kwargs.get("y")

    if x_col is None or y_col is None:
        raise ValueError("Please provide both x, y column names")

    s_x = data[x_col]
    s_y = data[y_col]

    return plt.plot(
        x=s_x.values,
        y=s_y.values,
        x_title=s_x.name,
        y_title=s_y.name,
    )


def hist_series(data, **kwargs):
    return plt.hist(x=data.values, x_title=data.name, **kwargs)


def boxplot_series(*args, **kwargs):
    raise NotImplementedError


def boxplot_frame(*args, **kwargs):
    raise NotImplementedError


def boxplot_frame_groupby(grouped, **kwargs):
    raise NotImplementedError


def hist_frame(*args, **kwargs):
    raise NotImplementedError
