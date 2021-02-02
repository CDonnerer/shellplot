"""Test config functionality
"""
import pytest

from shellplot._config import get_option, set_option


def test_option_set_and_get():
    new_figsize = (50, 30)
    set_option("figsize", new_figsize)
    figsize = get_option("figsize")
    assert figsize == new_figsize


def test_not_implemented_option():
    with pytest.raises(NotImplementedError):
        set_option("not-existing-option", 0)
