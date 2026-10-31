# Game loader tool module.
# This module has for purpose to load the game to allow its execution while avoiding cascading errors.

# Below are the imports.

import importlib.util
import os
from winstlib import flags

def ls(dir: str = "") -> list:
    """
    The command LS

    Args:
        dir: A directory.

    Returns:
        List of files and folders in this directory.

    """
    return os.listdir(dir)


def chk_recursive(dir: str = "") -> dict:
    """
    Check dirs recursively.

    Args:
        dir: A directory.

    Returns:
        Resursive list of files.
    """
    tree = {}
    contents = ls(dir)
    for elem in contents:
        if not elem in [".git", "__pycache__", ".venv"]:
            if os.path.isdir(os.path.join(dir, elem)):
                tree[elem] = chk_recursive(os.path.join(dir, elem))
            else:
                tree[elem] = "file"
    return tree

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
    if not path:
        path = name
    try:
        if path and os.path.exists(path):
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        else:
            pass
    except Exception as e:
        print(e)
        flags.raiseflag("LoadingError")
