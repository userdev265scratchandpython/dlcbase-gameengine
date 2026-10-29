# Logger module.
# This module's sole purpose is to log to stdout, alias the shell standard output, everything that is happening.
# This is meant to log
#  - timestamp
#  - caller(module)
#  - log level
#  - message

# Below are imports.

import datetime
import inspect
import sys

# Set log level

loglevel = "info"

# Detect loglevel param

if "--debug" in sys.argv:
    loglevel = "debug"
elif "--info" in sys.argv:
    loglevel = "info"
elif "--warn" in sys.argv:
    loglevel = "warn"
elif "--err" in sys.argv:
    loglevel = "err"

# Below is the code to log.

def log(message, level="INFO", module="__unknown__"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    module = module[:15].ljust(15)
    print(f"[{timestamp}] [{module}] [{level[:5].ljust(5)}] {message}")

# Below are the stubs for each loglevel.

def info(message):
    if loglevel in ["info", "debug"]:
        caller = inspect.currentframe().f_back
        module = caller.f_globals.get("__name__", "__unknown__").replace("__main__", sys.argv[0]).removesuffix(".py").replace(".", "/") + ".py"
        log(message, "INFO", module)

def warn(message):
    if loglevel in ["info", "debug", "warn"]:
        caller = inspect.currentframe().f_back
        module = caller.f_globals.get("__name__", "__unknown__").replace("__main__", sys.argv[0]).removesuffix(".py").replace(".", "/") + ".py"
        log(message, "WARN", module)

def error(message):
    if loglevel in ["info", "debug", "warn", "err"]:
        caller = inspect.currentframe().f_back
        module = caller.f_globals.get("__name__", "__unknown__").replace("__main__", sys.argv[0]).removesuffix(".py").replace(".", "/") + ".py"
        log(message, "ERROR", module)

def debug(message):
    if loglevel in ["debug"]:
        caller = inspect.currentframe().f_back
        module = caller.f_globals.get("__name__", "__unknown__").replace("__main__", sys.argv[0]).removesuffix(".py").replace(".", "/") + ".py"
        log(message, "DEBUG", module)
