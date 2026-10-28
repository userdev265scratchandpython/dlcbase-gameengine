# Flags management module.
# This module's sole purpose is to manage flags so the game engine can run properly.
# There are no imports used here.

# Below is the code to raise a flag. A flag cannot be unraised.

def raiseflag(flag):
    global _flags
    try:
        if _flags[flag] == True:
            print(f"No need to re-raise flag \"{flag}\".")
        else:
            print(f"Raised flag \"{flag}\".")
            _flags[flag] = True
    except:
        print(f"No such known flag \"{flag}\".")

# Below is the code to read a flag.

def getflag(flag):
    global _flags
    return _flags[flag]

# Below is the code to initialize flags.

def initflags(flagslist):
    global _flags
    _flags = {}
    try:
        for flag in flagslist:
            _flags[flag] = False
        return True
    except:
        _flags = {}
        return False
