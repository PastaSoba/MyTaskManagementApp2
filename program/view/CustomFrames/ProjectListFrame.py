import tkinter as tk
import tkinter.ttk as ttk



class ProjectListFrame:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.config(background='blue')
        self.frame.pack(fill=tk.BOTH, expand=True)
