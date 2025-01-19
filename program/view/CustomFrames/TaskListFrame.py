import tkinter as tk
import tkinter.ttk as ttk



class TaskListFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.config(background='green')
        self.frame.pack(fill=tk.BOTH, expand=True)