"""API for pandas plotting backend
"""

import shellplot.plots as plt


def plot(data, kind, **kwargs):
    # TODO: check kind

    s_x = data[kwargs["x"]]
    s_y = data[kwargs["y"]]

    return plt.plot(
        x=s_x.values,
        y=s_y.values,
        x_title=s_x.name,
        y_title=s_y.name,
    )


def hist_series(data, **kwargs):
    return plt.hist(
        x=data.values,
        x_title=data.name,
        **kwargs
    )
