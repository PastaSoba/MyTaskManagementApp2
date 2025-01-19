import tkinter as tk
import tkinter.ttk as ttk



class DetailFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)