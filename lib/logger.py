import datetime
import inspect

def log(message, level="INFO", module="__unknown__"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    module = module[:15].ljust(15)
    print(f"[{timestamp}] [{module}] [{level[:5].ljust(5)}] {message}")

def info(message):
    caller = inspect.currentframe().f_back
    module = caller.f_globals.get("__name__", "__unknown__")
    log(message, "INFO", module)

def warn(message):
    caller = inspect.currentframe().f_back
    module = caller.f_globals.get("__name__", "__unknown__")
    log(message, "WARN", module)

def error(message):
    caller = inspect.currentframe().f_back
    module = caller.f_globals.get("__name__", "__unknown__")
    log(message, "ERROR", module)

def debug(message):
    caller = inspect.currentframe().f_back
    module = caller.f_globals.get("__name__", "__unknown__")
    log(message, "DEBUG", module)
