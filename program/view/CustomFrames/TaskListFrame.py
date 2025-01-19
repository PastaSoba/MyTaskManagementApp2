import tkinter as tk
import tkinter.ttk as ttk



class TaskListFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.add_task_button = ttk.Button(self.frame, text="+ Add Task")
        self.add_task_button.pack(side=tk.BOTTOM, fill="x")