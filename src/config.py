import time
from aqt import mw
from functools import lru_cache


def _get_cache_key():
    return round(time.time() / 2)

@lru_cache()
def _get_config(cache_key):
    return mw.addonManager.getConfig(__name__)

def get_config_value(key):
    config = _get_config(_get_cache_key())
    try:
        return config[key]
    except (KeyError, TypeError):
        return None

def update_config(key, value):
    config = _get_config(_get_cache_key())
    config[key] = value
    mw.addonManager.writeConfig(__name__, config)
