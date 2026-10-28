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

def getflag(flag):
    global _flags
    return _flags[flag]

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
