# Flags management module.
# This module's sole purpose is to manage flags so the game engine can run properly.

# Below are the imports.

from winstlib import logger

# Below is initialization for information, debug and wan stubs.

info = logger.info
debug = logger.debug
warn = logger.warn

# Below is the code to raise a flag. A flag cannot be unraised.

def raiseflag(flag: str) -> bool:
    """
    Raises a flag initialized from initflags.
    Can be used by import.
    Takes the flag argument, a string of the flag's name.
    Returns its success status.
    """
    global _flags, info, debug, warn
    try:
        if _flags[flag] == True:
            debug(f"No need to re-raise flag \"{flag}\".")
        else:
            info(f"Raised flag \"{flag}\".")
            _flags[flag] = True
            return True
    except:
        warn(f"No such known flag \"{flag}\".")
    return False

# Below is the code to read a flag.

def getflag(flag: str) -> bool:
    """
    reads from _flags
    Reads a flag initialized from initflags()
    Can be used by import.
    Takes the flag argument, a string of the flag's name.
    Returns the flag's raise status(via raiseflag()) if existant or None.
    """
    global _flags, info, debug, warn
    if flag in _flags:
        return _flags[flag]
    else:
        warn("Flag does not exist. Returning None.")
        return False

# Below is the code to initialize flags.

def initflags(flagslist: list) -> bool:
    """
    Initializes flags from a list of strings.
    Can be used by import.
    Returns its success state(True or False).
    """
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
