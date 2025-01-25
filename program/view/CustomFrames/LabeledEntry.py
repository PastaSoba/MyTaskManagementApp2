import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional



class LabeledEntry:
    """ラベル(Label)とエントリ(Entry)を組み合わせたフレーム(Frame)"""
    def __init__(self, parent, label_value: str=""):
        # ラベルとエントリを持つフレームを作成
        self.frame : ttk.Frame = ttk.Frame(parent)
        self.label : ttk.Label = ttk.Label(self.frame, text=label_value)
        self.entry : ttk.Entry = ttk.Entry(self.frame)
        # ラベルとエントリをフレームに配置
        self.frame.pack(fill=tk.BOTH)
        self.label.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT, fill="x")


    def set(self, value: str):
        """エントリに値を設定する
        """
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

    def get(self) -> str:
        """エントリの値を取得する
        """
        return self.entry.get()