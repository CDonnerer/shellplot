# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

from shellplot import pandas_api  # noqa: F401

from shellplot.plots import plot, hist  # noqa: F401

from shellplot.utils import load_dataset  # noqa: F401
