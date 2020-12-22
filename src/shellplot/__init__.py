# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound, get_distribution

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


# -----------------------------------------------------------------------------
# Expose imports to be directly available via import shellplot as plt
# -----------------------------------------------------------------------------

from shellplot import pandas_api  # noqa: F401
from shellplot.plots import barh, boxplot, hist, plot  # noqa: F401
from shellplot.utils import load_dataset  # noqa: F401
