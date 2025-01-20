import tkinter as tk
import tkinter.ttk as ttk



class DetailFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self._type_label = ttk.Label(self.frame, text="オブジェクトのタイプ") # testcode
        self._name_label = ttk.Label(self.frame, text="オブジェクトの名前")   # testcode


        self._type_label.pack(side=tk.TOP, fill="x", padx=10, pady=10) # testcode
        self._name_label.pack(side=tk.TOP, fill="x", padx=10, pady=10) # testcode
        self.frame.pack(fill=tk.BOTH, expand=True)