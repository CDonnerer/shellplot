# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for shellplot.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import pytest

from shellplot.utils import load_dataset


@pytest.fixture
def df_penguins():
    return load_dataset("penguins")
