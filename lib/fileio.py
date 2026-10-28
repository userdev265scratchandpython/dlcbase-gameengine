from lib import flags
from lib import logger
queue = ""
def print(text, end="\n"):
    global queue
    if end.endswith("\n"):
        logger.debug(f"{queue}{text}{end}".rstrip("\n"))
        queue = ""
    else:
        queue = f"{queue}{text}"
import os
_open = open
class exfile:
    def __init__(self):
        pass
    def read(self):
        return ""
    def write(self, data):
        print("Skipped write.")
    def close(self):
        print("Nothing to close")
class fileobject:
    def __init__(self, filepath="", mode="r"):
        if filepath and os.path.exists(filepath):
            if mode == "r":
                print(text=f"Opening \"{filepath}\" readonly... ", end="")
                try:
                    self.file = _open(filepath, "r")
                    self.mode = "read"
                    print(text="OK")
                except Exception as e:
                    print(text="An error occured. Refusing to continue.")
                    print(text=e)
                    flags.raiseflag("FileError")
            elif mode == "rw":
                print(text=f"Opening \"{filepath}\" readwrite... ", end="")
                try:
                    self.file = _open(filepath, "r+")
                    self.mode = "readwrite"
                    print(text="OK")
                except Exception as e:
                    print(text="An error occured. Refusing to continue.")
                    print(text=e)
                    flags.raiseflag("FileError")
            elif mode == "w":
                print(text=f"Opening \"{filepath}\" writeonly... ", end="")
                try:
                    self.file = _open(filepath, "w")
                    self.mode = "write"
                    print(text="OK")
                except Exception as e:
                    print(text="An error occured. Refusing to continue.")
                    print(text=e)
                    flags.raiseflag("FileError")
            else:
                print(text=f"Unsupported mode: \"{mode}\". Refusing to continue.")
                flags.raiseflag("FileError")
        else:
            print("The file requested does not exist. Making our example to avoid crashes.")
            self.mode = "readwrite"
            self.file = exfile()
    def read(self, count=0):
        try:
            if "read" in self.mode:
                if type(count).__name__ == "int":
                    if count == 0:
                        return self.file.read()
                    else:
                        return self.file.read(count)
                else:
                    flags.raiseflag("FileError")
                    return self.file.read()
            else:
                flags.raiseflag("FileError")
        except Exception as e:
            print(text=e)
            flags.raiseflag("FileError")
            return False
    def write(self, content):
        try:
            if "write" in self.mode:
                if type(content).__name__ == "str":
                    self.file.write(content)
                    return True
                else:
                    flags.raiseflag("FileError")
            else:
                flags.raiseflag("FileError")
        except:
            flags.raiseflag("FileError")
        return False
    def close(self):
        self.file.close()
        self.mode = ""
        del self.mode
        del self.file
def open(fp="", mode="r"):
    return fileobject(filepath=fp, mode=mode)
