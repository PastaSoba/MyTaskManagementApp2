import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional
from model.model import Project



class ProjectListFrame:
    def __init__(self, parent):
        self.frame              : ttk.Frame              = ttk.Frame(parent)
        self._project_treeview   : Optional[ttk.Treeview] = None # プロジェクト一覧
        self._add_project_button : Optional[ttk.Button]   = None # プロジェクト追加ボタン


        self.frame.pack(fill=tk.BOTH, expand=True)
        self.__create_project_treeview()
        self.__create_add_project_button()
        self.__create_right_click_menu()


    def __create_project_treeview(self):
        """プロジェクト一覧を表示するTreeviewを作成して、frameに配置する
        """
        self._project_treeview = ttk.Treeview(self.frame, columns=["name"], show="headings")
        self._project_treeview.heading("name", text="Project Name")
        self._project_treeview.column("name", width=150)
        self._project_treeview.pack(side=tk.TOP, fill="both", expand=True)

    def __create_add_project_button(self):
        """プロジェクト追加ボタンを作成して、frameに配置する
        """
        self._add_project_button = ttk.Button(self.frame, text="+ Add Project")
        self._add_project_button.pack(side=tk.BOTTOM, fill="x")

    def __create_right_click_menu(self):
        """
        右クリックメニューのひな形と、 Treeview上で右クリックすることで
        メニューを表示するイベントを設定する。
        
        NOTE: このメソッドではあくまで「ひな形」しか作らない。
              メニューの内容とそれに対応するイベントハンドラはControllerで設定される
        """
        self._right_click_menu = tk.Menu(self.frame, tearoff=0)
        def show_right_click_menu(event):
            selected_row = self._project_treeview.identify_row(event.y)
            if selected_row:
                self._project_treeview.selection_set(selected_row)
                self._right_click_menu.post(event.x_root, event.y_root)
        self._project_treeview.bind("<Button-3>", show_right_click_menu)

    def add_project_row(self, project: Project):
        """プロジェクト一覧を表示するTreeViewにプロジェクトを表す行を追加する
        """
        # treeview中の行も、project.idで識別できるようにしてある
        self._project_treeview.insert("", "end", iid=project.id, values=(project.name,))

    def update_project_row(self, project: Project):
        """プロジェクト一覧を表示するTreeViewのプロジェクトを表す行を更新する
        """
        self._project_treeview.item(project.id, values=(project.name,))

    def add_project_rows(self, projects: list[Project]):
        """プロジェクト一覧を表示するTreeViewに複数のプロジェクトを表す行を追加する
        """
        for project in projects:
            self.add_project_row(project)