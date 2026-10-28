import tkinter as tk
import threading
def report_exception(exc, val, tb):
    raise Exception(f"Tkinter callback failed: {val}")
def err():
    raise Exception("Asked to crash")
def exwindow():
    root = tk.Tk()
    root.report_callback_exception = report_exception
    root.geometry("1500x850")
    root.resizable(False, False)
    label = tk.Label(root, text="Hello, world!")
    label.grid(row=0, column=0, padx=0, pady=0)
    button = tk.Button(root, text="Hello, world!", command=err)
    button.grid(row=1, column=0, padx=0, pady=0)
    root.mainloop()
