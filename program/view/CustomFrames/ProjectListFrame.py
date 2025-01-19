import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional



class ProjectListFrame:
    def __init__(self, parent):
        self.frame              : ttk.Frame              = ttk.Frame(parent)
        self.project_treeview   : Optional[ttk.Treeview] = None # プロジェクト一覧
        self.add_project_button : Optional[ttk.Button]   = None # プロジェクト追加ボタン


        self.frame.pack(fill=tk.BOTH, expand=True)
        self.__create_project_treeview()
        self.__create_add_project_button()


    def __create_project_treeview(self):
        """プロジェクト一覧を表示するTreeviewを作成して、frameに配置する
        """
        self.project_treeview = ttk.Treeview(self.frame, columns=["name"], show="headings")
        self.project_treeview.heading("name", text="Project Name")
        self.project_treeview.column("name", width=200)
        self.project_treeview.pack(side=tk.TOP, fill="both", expand=True)

    def __create_add_project_button(self):
        """プロジェクト追加ボタンを作成して、frameに配置する
        """
        self.add_project_button = ttk.Button(self.frame, text="+ Add Project")
        self.add_project_button.pack(side=tk.BOTTOM, fill="x")