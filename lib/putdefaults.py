# Crash avoider by putting defaults.
# This module adds default keys if unset to avoid a crash.
# This only gets it to say what you did wrong instead of yelling at you.

def add(cfg: dict = None, data: list = [["ExKey", ["ExVal0", "ExVal1"]], ["ExKey2": str, "ExVal0"]]) -> dict:
    """Brief description of add.

    Args:
        cfg: Phrased configuration.
        data: Default keys and values.

    Returns:
        Configuration with defaults for missing keys.

    """
    if cfg is None:
        cfg = {}
    config = cfg
    for elem in data:
        if elem[0] in config:
            pass
        else:
            config[elem[0]] = elem[1]
    return config