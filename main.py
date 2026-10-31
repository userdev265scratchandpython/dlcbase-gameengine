# Main code. This should be run.
# This is mostly a wrapper.

# Importing the flags manager.
from winstlib import flags                  # flags.initflags, flags.raiseflag, flags.getflag

# Initializing flags.

# Set default flags
_flags = ["LoadingError", "FileError", "PhraseError"]
# set full flags list(will be filled)
flagsfull = []
# iterate over all flags and the engine quit one
for flagsl in [_flags, ["EngineWillQuit"]]:
    for flag in flagsl:
        # add the flags to the full flags list
        flagsfull.append(flag)

if flags.initflags(flagsfull):
    pass
else:
    exit()

# Importing other dependencies once flags are initialized.

from winstlib import fileio                 # fileio.open
from winstlib import loadtool               # loadtool.importmod
from winstlib import phrasetool             # phrasetool.phrase_w
from winstlib import putdefaults            # putdefaults.add
from winstlib import gamelib                # nothing used, just to inject to games
from winstlib import logger                 # logging :)
import os                              # just to check if a file exists...
from importlib.metadata import version # Get pip version


# allow quicker use of the stubs from logger with slight overhead.

info = logger.info
warn = logger.warn
error = logger.error
debug = logger.debug

# Make sure pip is safe
pip_version = tuple(map(int, version("pip").split(".")))
info(f"Pip version : {version("pip")}")
if pip_version <= (26, 2, 1):
    print("Please update pip before running this.")
    flags.raiseflag("EngineWillQuit")


# Avoid bad flags getting through.

def chk_ok():
    """
    Checks if the flags are raised and returns True if any is.

    Returns:
        True if any flag is raised, False otherwise.

    """
    # Verify each known flag.
    # use only flags other than EngineWillQuit
    for flag in _flags:
        if flags.getflag(flag):
            # Return True(ErrorHappened) if any helper flag error happened.
            return True
    # Return False otherwise.
    return False

# log the start of the loading.

info("Loading DLCbase game... ")

# Load the configuration.

lines = fileio.open(fp="dlc/game.w", mode="r").read().splitlines()

# Phrase configuration.

config = phrasetool.phrase_w(lines)

# Apply defaults for unset keys. This should often say 3 things were skipped.

config = putdefaults.add(cfg=config, data=[["mainfile", ""], ["mainfunction", "main"], ["package", "err.unset.pkg"]])

# Extract package name, main file path and main function to render access easier.

debug("Ectract info")

package = config["package"]
mainfile = config["mainfile"]
mainfunct = config["mainfunction"]

# Verify all information is there.

if package == "":
    error("No package name was set.")
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")
if mainfile == "":
    error("No main file supplied")
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")
if mainfunct == "":
    error("No main function supplied")
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")

# Avoid an useless crash.

if chk_ok():
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")

if flags.getflag("EngineWillQuit"):
    exit()

# Verify if the main file exists.

if not os.path.exists(mainfile):
    error("Main file does not exist.")
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")

# Same as before, avoid an useless crash.

if chk_ok():
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")

if flags.getflag("EngineWillQuit"):
    exit()

# Inform the user of what is running.

info("======")
info(f"== Running package : {package}")
info("======")

# Make sure the code doesn't try to commit suidide.

lines = fileio.open(fp=mainfile, mode="r").read().splitlines()
if "import gamelib" in lines:
    warn("Importing gamelib is unsupported. Your code will likely error out.")
    warn("This could also be unrelated to the actual code and may just be a mistake.")

# Attempt to load the game.

try:
    game = loadtool.importmod(name="mod", path=mainfile)
    debug("Read game")
    game.gamelib = gamelib
    debug("Injected gamelib library")
except Exception as e:
    # Handle errors.
    print(e)
    error("Error loading game")
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")

# Once again, avoid a crash.

if chk_ok():
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")

if flags.getflag("EngineWillQuit"):
    exit()

# Verify the existance of the requested main function to attempt to run it if exists, when ready.
if hasattr(game, mainfunct):
    debug("Running game")
    try:
        info("===== Game execution start")
        getattr(game, mainfunct)()
        info("===== Game execution end")
        debug("Game closed successfully")
    except Exception as e:
        # handle errors.
        error("Game errored out: ")
        error(e)
else:
    # Avoid running nonexistant code.
    debug("Supplied main function does NOT exist.")