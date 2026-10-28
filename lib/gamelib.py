# Game library.
# This module's whole purpose is to be injected into a game to be used by said game.

# Below are the imports.

import tkinter as tk
import threading

# Below is a workaround used because Python tkinter sucks

def report_exception(exc, val, tb):
    raise Exception(f"Tkinter callback failed: {val}")

# Below is a stub to raise an error because it's easier that way.

def err():
    raise Exception("Asked to crash")

# Below is the code to initialize a window.

def exwindow():
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
