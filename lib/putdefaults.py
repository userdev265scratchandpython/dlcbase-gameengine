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