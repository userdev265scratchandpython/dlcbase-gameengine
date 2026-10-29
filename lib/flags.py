# Flags management module.
# This module's sole purpose is to manage flags so the game engine can run properly.

# Below are the imports.

from lib import logger

# Below is initialization for information, debug and wan stubs.

info = logger.info
debug = logger.debug
warn = logger.warn

# Below is the code to raise a flag. A flag cannot be unraised.

def raiseflag(flag):
    global _flags, info, debug, warn
    try:
        if _flags[flag] == True:
            debug(f"No need to re-raise flag \"{flag}\".")
        else:
            info(f"Raised flag \"{flag}\".")
            _flags[flag] = True
    except:
        warn(f"No such known flag \"{flag}\".")

# Below is the code to read a flag.

def getflag(flag):
    global _flags, info, debug, warn
    if flag in _flags:
        return _flags[flag]
    else:
        warn("Flag does not exist. Returning None.")
        return none

# Below is the code to initialize flags.

def initflags(flagslist):
    global _flags, info, debug, warn
    _flags = {}
    try:
        for flag in flagslist:
            debug(f"Initialized flag : {flag}")
            _flags[flag] = False
        return True
    except:
        info("Could not initialize flags.")
        _flags = {}
        return False
