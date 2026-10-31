# Game loader tool module.
# This module has for purpose to load the game to allow its execution while avoiding cascading errors.

# Below are the imports.

import importlib.util
import os
from winstlib import flags

# Below is the code to import the game module and send it to the caller.

def importmod(name: str = "hi", path: str = "") -> Any:
    """
    Imports a module.

    Args:
        name: used for importlib, not critical to change.
        path: Path of module.

    Returns:
        The imported module.

    """
    try:
        if path and os.path.exists(path):
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(e)
        flags.raiseflag("LoadingError")
