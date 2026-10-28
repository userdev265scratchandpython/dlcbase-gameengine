import importlib.util
import os
from lib import flags

def importmod(name="hi", path=""):
    try:
        if path and os.path.exists(path):
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(e)
        flags.raiseflag("LoadingError")
