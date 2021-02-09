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

__figure_doc = """figsize : a tuple (width, height) in ascii characters, optional
        Size of the figure.
    xlim : 2-tuple/list, optional
        Set the x limits.
    ylim : 2-tuple/list, optional
        Set the y limits.
    xlabel : str, optional
        Name to use for the xlabel on x-axis.
    ylabel : str, optional
        Name to use for the ylabel on y-axis.
    label : str/ list of str, optional
        Labels that make the figure legend
    return_type : str, optional
        If `'str'`, returns the plot as a string. Otherwise, the plot will be
        directly printed to stdout.

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

        func_fig_doc.__doc__ = inspect.getdoc(getattr(Figure, fig_func))
        # + inspect.cleandoc(__figure_doc)
        return func_fig_doc

    return decorate


@add_fig_doc("plot")
def plot(x, y, color=None, fig=None, **kwargs):
    x_label, y_label = get_label(x), get_label(y)

    if isinstance(y_label, list):  # multi label goes into legend
        if kwargs.get("label") is None:
            kwargs.update({"label": y_label})
    elif isinstance(y_label, str):  # single label goes into axis labels
        if kwargs.get("ylabel") is None:
            kwargs.update({"ylabel": y_label})
        if kwargs.get("xlabel") is None:
            kwargs.update({"xlabel": x_label})

    fig, show = validate_fig(fig, **kwargs)

    fig.plot(x, y, color=color, **kwargs)

    return return_plt(fig, show, **kwargs)


@add_fig_doc("hist")
def hist(x, bins=10, fig=None, **kwargs):
    if kwargs.get("xlabel") is None:
        kwargs.update({"xlabel": get_label(x)})
    if kwargs.get("ylabel") is None:
        kwargs.update({"ylabel": "counts"})

    fig, show = validate_fig(fig, **kwargs)

    fig.hist(x, bins=bins, **kwargs)

    return return_plt(fig, show, **kwargs)


@add_fig_doc("barh")
def barh(x, labels=None, fig=None, **kwargs):
    kwargs.update({"xlabel": get_label(x)})

    fig, show = validate_fig(fig, **kwargs)

    fig.barh(x, labels=labels, **kwargs)

    return return_plt(fig, show, **kwargs)


@add_fig_doc("boxplot")
def boxplot(x, labels=None, fig=None, **kwargs):
    if labels is None:
        labels = get_label(x)

    fig, show = validate_fig(fig, **kwargs)

    fig.boxplot(x, labels=labels, **kwargs)

    return return_plt(fig, show, **kwargs)


def validate_fig(fig, **kwargs):
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
