# Crash avoider by putting defaults.
# This module adds default keys if unset to avoid a crash.
# This only gets it to say what you did wrong instead of yelling at you.

def add(cfg=None, data=[["ExKey", ["ExVal0", "ExVal1"]], ["ExKey2", "ExVal0"]]):
    if cfg is None:
        cfg = {}
    config = cfg
    for elem in data:
        if elem[0] in config:
            pass
        else:
            config[elem[0]] = elem[1]
    return config