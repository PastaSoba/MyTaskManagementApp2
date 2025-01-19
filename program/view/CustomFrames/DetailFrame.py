import tkinter as tk
import tkinter.ttk as ttk



class DetailFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.config(background='red')
        self.frame.pack(fill=tk.BOTH, expand=True)