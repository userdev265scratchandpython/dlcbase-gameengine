from lib import flags       # flags.initflags, flags.raiseflag, flags.getflag
flags.initflags([
    "LoadingError", "FileError", "PhraseError", "EngineWillQuit"
])
from lib import fileio      # fileio.open
from lib import loadtool    # loadtool.importmod
from lib import phrasetool  # phrasetool.phrase_w
from lib import putdefaults # putdefaults.add
from lib import gamelib     # nothing used, just to inject to games
from lib import logger      # logging :)
import os
info = logger.info
warn = logger.warn
error = logger.error
debug = logger.debug
info("Loading DLCbase game... ")
lines = fileio.open(fp="dlc/game.w", mode="r").read().splitlines()
config = phrasetool.phrase_w(lines)
config = putdefaults.add(cfg=config, data=[["mainfile", ""], ["mainfunction", "main"], ["package", "err.unset.pkg"]])
package = config["package"]
mainfile = config["mainfile"]
mainfunct = config["mainfunction"]
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
if flags.getflag("EngineWillQuit"):
    exit()
if not os.path.exists(mainfile):
    error("Main file does not exist.")
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")
if flags.getflag("EngineWillQuit"):
    exit()
info("======")
info(f"== Running package : {package}")
info("======")
lines = fileio.open(fp=mainfile, mode="r").read().splitlines()
if "import gamelib" in lines:
    warn("Importing gamelib is unsupported. Your code will likely error out.")
try:
    game = loadtool.importmod(name="mod", path=mainfile)
    debug("Read game")
    game.gamelib = gamelib
    debug("Injected gamelib library")
except Exception as e:
    print(e)
    error("Error loading game")
    if not flags.getflag("EngineWillQuit"):
        flags.raiseflag("EngineWillQuit")
if flags.getflag("EngineWillQuit"):
    exit()
if hasattr(game, mainfunct):
    debug("Running game")
    try:
        getattr(game, mainfunct)()
        debug("Game closed successfully")
    except Exception as e:
        error("Game errored out: ")
        print(e)
else:
    debug("Supplied main function does NOT exist.")