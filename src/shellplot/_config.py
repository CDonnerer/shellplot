"""
Configuration options for shellplot
"""
from typing import Any, Dict

_global_config: Dict[str, Any] = {"figsize": (71, 27)}

_available_keys = _global_config.keys()


def get_option(key):
    return _global_config[key]


def set_option(key, value):
    if key not in _available_keys:
        raise NotImplementedError(
            f"Option not available! Please use one of {_available_keys}"
        )
    _global_config[key] = value
