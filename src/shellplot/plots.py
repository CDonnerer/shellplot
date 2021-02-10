"""Functional API for shellplot
"""
import inspect
from functools import wraps

from shellplot.figure import Figure, figure
from shellplot.utils import get_label

__all__ = ["plot", "hist", "barh", "boxplot"]


# -----------------------------------------------------------------------------
# Exposed functions that directly print the plot
# -----------------------------------------------------------------------------

__figure_doc = """
    fig : `shellplot.figure.Figure`, optional, default None
        If provided, plot will be attached to figure. Otherwise, a new figure
        is created for the plot
    return_type : str, optional
        If `'str'`, returns the plot as a string. Otherwise, the plot will be
        directly printed to stdout.
    **kwargs
        Additional parameters passed to `shellplot.figure`
        (Only used if the fig keyword is None)

    Returns
    -------
    result
        See notes, dependent on `return_type`
"""


def add_fig_doc(fig_func="plot"):
    def decorate(func):
        """Add figure params to docstring of func"""

        @wraps(func)
        def func_fig_doc(*args, **kwargs):
            return func(*args, **kwargs)

        func_fig_doc.__doc__ = (
            inspect.getdoc(getattr(Figure, fig_func))
            + "\n"
            + inspect.cleandoc(__figure_doc)
        )
        return func_fig_doc

    return decorate


@add_fig_doc("plot")
def plot(x, y, fig=None, **kwargs):
    x_label, y_label = get_label(x), get_label(y)

    if isinstance(y_label, list):  # multi label goes into legend
        if kwargs.get("label") is None:
            kwargs.update({"label": y_label})
    elif isinstance(y_label, str):  # single label goes into axis labels
        if kwargs.get("ylabel") is None:
            kwargs.update({"ylabel": y_label})
        if kwargs.get("xlabel") is None:
            kwargs.update({"xlabel": x_label})

    fig, show = check_fig(fig, **kwargs)

    fig.plot(x, y, **kwargs)

    return return_plt(fig, show, **kwargs)


@add_fig_doc("hist")
def hist(x, bins=10, fig=None, **kwargs):
    if kwargs.get("xlabel") is None:
        kwargs.update({"xlabel": get_label(x)})
    if kwargs.get("ylabel") is None:
        kwargs.update({"ylabel": "counts"})

    fig, show = check_fig(fig, **kwargs)

    fig.hist(x, bins=bins, **kwargs)

    return return_plt(fig, show, **kwargs)


@add_fig_doc("barh")
def barh(x, labels=None, fig=None, **kwargs):
    kwargs.update({"xlabel": get_label(x)})

    fig, show = check_fig(fig, **kwargs)

    fig.barh(x, labels=labels, **kwargs)

    return return_plt(fig, show, **kwargs)


@add_fig_doc("boxplot")
def boxplot(x, labels=None, fig=None, **kwargs):
    if labels is None:
        labels = get_label(x)

    fig, show = check_fig(fig, **kwargs)

    fig.boxplot(x, labels=labels, **kwargs)

    return return_plt(fig, show, **kwargs)


def check_fig(fig, **kwargs):
    """Check if figure is included in kwargs. Otherwise, creates a new fig"""
    show = False
    if fig is None:
        fig = figure(**kwargs)
        show = True
    return fig, show


def return_plt(fig, show, **kwargs):
    if show:
        if kwargs.get("return_type") == "str":
            return fig.draw()
        else:
            fig.show()
