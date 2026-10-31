# Game library.
# This module's whole purpose is to be injected into a game to be used by said game.

# Below are the imports.

import tkinter as tk
import threading
from winstlib import logger

# Define stubs for output

info = logger.info
warn = logger.warn
debug = logger.debug
error = logger.error

info("Loaded GameLIB")

# Below is a workaround used because Python tkinter sucks

def report_exception(exc: Any, val: Any, tb: Any) -> None:
    """
    Catch an error instead of tkinter.

    Args:
        exc: Dunno, GPT made this to help me fix tkinter not letting me crash stuff.
        val: Dunno, GPT made this to help me fix tkinter not letting me crash stuff.
        tb: Dunno, GPT made this to help me fix tkinter not letting me crash stuff.

    Returns:
        nothing
    """
    raise Exception(f"Tkinter callback failed: {val}")

# Below is a stub to raise an error because it's easier that way.

def err():
    """
    Raises an error.

    Returns:
        nothing

    """
    raise Exception("Asked to crash")

# Below is the code to initialize a window.

def exwindow():
    """
    Opens an example window

    Returns:
        nothing

    """
    root = tk.Tk()
    # The line below uses the workaround stub so tkinter doesn't catch the error.
    root.report_callback_exception = report_exception
    root.geometry("1500x850")
    root.resizable(False, False)
    label = tk.Label(root, text="Hello, world!")
    label.grid(row=0, column=0, padx=0, pady=0)
    # The line below uses the error-raising stub.
    button = tk.Button(root, text="Crash the app!!!", command=err)
    button.grid(row=1, column=0, padx=0, pady=0)
    root.mainloop()
