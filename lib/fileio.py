# File input-output module.
# This module's sole purpose is to read and write files while avoiding fatal errors.

# Below are imports.

from lib import flags
from lib import logger
import os

# Below is the definition of the code to queue outputs if needed or pass them directly.

queue = ""
def print(text: str, end: str = "\n") -> None:
    global queue
    if end.endswith("\n"):
        logger.debug(f"{queue}{text}{end}".rstrip("\n"))
        queue = ""
    else:
        queue = f"{queue}{text}"

# Below is the code that avoids a recursive error mess.

_open = open

# Below is the definition of a demo, stub, empty, useless, crash avoider file object.

class exfile:
    def __init__(self):
        """
        Does:
            nothing
        """
        pass
    def read(self):
        """
        Returns:
            nothing
        """
        return ""
    def write(self, data: str) -> None:
        """
        does nothing

        Args:
            data: string.

        Returns:
            nothing

        """
        print("Skipped write.")
    def close(self):
        """
        Returns:
            nothing
        """
        print("Nothing to close")

# Below is the definition of the exposed file object.

class fileobject:
    # Below is the code to open a file, referencing to the exfile stub in case of an issue.
    # It supports read, read+write and just write.
    # mode is on request.
    def __init__(self, filepath: str = "", mode: str = "r") -> None:
        """
        Opens a file with a mode.

        Args:
            filepath: A file's path.
            mode: any mode in the following list: r, rw, w.

        Returns:
            None, the class is returned

        """
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
    # Below is the code to read a read-enabled file.
    def read(self, count: int = 0) -> str:
        """
        Read a file if possible

        Args:
            count: amount of characters.

        Returns:
            Data returned by the real python file object.

        """
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
            return ""
    # Below is the code to write to a write enabled file.
    def write(self, content: str = "") -> bool:
        """
        Write to a file if possible.

        Args:
            content: Content to write.

        Returns:
            Success status.

        """
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
    # Below is the code to close the file safely.
    def close(self):
        """
        Closes the file

        Returns:
            nothing

        """
        self.file.close()
        self.mode = ""
        del self.mode
        del self.file

# Below is the stub to open a file easier. It is not required to use it but strongly recommended.

def open(fp: str = "", mode: str = "r") -> fileobject:
    """
    Open a flileobject

    Args:
        fp: the path of the file.
        mode: any of the following: r, rw, w.

    Returns:
        an initialized fileobject that can read(if mode allows it) or write(if mode allows it).

    """
    return fileobject(filepath=fp, mode=mode)
