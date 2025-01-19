import tkinter as tk
import tkinter.ttk as ttk



class ProjectListFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.add_project_button = ttk.Button(self.frame, text="+ Add Project")
        self.add_project_button.pack(side=tk.BOTTOM, fill="x")