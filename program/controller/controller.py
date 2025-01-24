from uuid import UUID

from model.model import ProjectRoot
from view.view import MainWindow
from tkinter import messagebox



class Controller:
    """コントローラークラス。シングルトンパターンを適用している。
    """
    _instance = None

    def __new__(cls, model:ProjectRoot, view:MainWindow):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model:ProjectRoot, view:MainWindow):
        self.model = model
        self.view  = view

        # ビューのイベントハンドラを設定
        self.view._project_list_frame._project_treeview.bind("<ButtonRelease>", self.__on_project_treeview_select)
        self.view._task_list_frame._task_treeview.bind("<ButtonRelease>", self.__on_task_treeview_select)
        self.view._project_list_frame._add_project_button.bind("<ButtonRelease>", self.__on_add_project_button_click)
        self.view._task_list_frame._add_task_button.bind("<ButtonRelease>", self.__on_add_task_button_click)

        self.__construct_initial_view() # 初期状態のビューを構築

    def __construct_initial_view(self):
        """初期状態のビューを構築する
        """
        # プロジェクト一覧とタスク一覧を取得
        projects = self.model.get_children()
        # view._project_list_frameにプロジェクト一覧を表示
        self.view._project_list_frame.add_project_rows(projects)

    def __on_project_treeview_select(self, event):
        """プロジェクト一覧のTreeViewで行が選択された際の処理

        1. 選択されたプロジェクトのタスク一覧を取得
        2. view._task_list_frameのタスク一覧表示を更新
        3. view._detail_frameの表示を更新
        """
        selected_project_id = UUID(self.view._project_list_frame._project_treeview.selection()[0])
        selected_project = self.model.get_child_by_id(selected_project_id)
        self.view._task_list_frame.delete_all_task_rows()
        self.view._task_list_frame.add_task_rows(selected_project.get_children())
        self.view._detail_frame._name_label["text"] = selected_project.name # testcode

    def __on_task_treeview_select(self, event):
        """タスク一覧のTreeViewで行が選択された際の処理

        A. タスクが選択された場合
            1. 選択されたタスクの詳細をview._detail_frameに表示
            2. view._detail_frameの表示を更新

        B. タスク以外の場所がクリックされた場合
            1. 選択を解除
        """
        if not self.view._task_list_frame._task_treeview.identify_row(event.y):
            # タスク以外の場所がクリックされた場合は選択を解除
            self.view._task_list_frame._task_treeview.selection_remove(*self.view._task_list_frame._task_treeview.selection())
            return
        selected_task_id = UUID(self.view._task_list_frame._task_treeview.selection()[0])
        selected_task = self.model.get_child_by_id(selected_task_id, recursive=True)
        self.view._detail_frame._name_label["text"] = selected_task.name # testcode

    def __on_add_project_button_click(self, event):
        """プロジェクト追加ボタンがクリックされた際の処理

        1. モデルに新しいプロジェクトを追加
        2. view._project_list_frameに新しいプロジェクトを表示
        """
        new_project = self.model.create_child()
        new_project.name = "New Project"
        self.view._project_list_frame.add_project_row(new_project)
        self.view._detail_frame._name_label["text"] = new_project.name # testcode

    def __on_add_task_button_click(self, event):
        """タスク追加ボタンがクリックされた際の処理

        1. 選択されているプロジェクトに新しいタスクを追加
        2. view._task_list_frameに新しいタスクを表示
        """
        if len(self.view._project_list_frame._project_treeview.selection()) == 0:
            # タスクの親となるべきプロジェクトが選択されていない場合は警告を表示
            messagebox.showwarning("Error", "No parental project is selected")
        else:
            selected_project_id = UUID(self.view._project_list_frame._project_treeview.selection()[0])
            selected_project = self.model.get_child_by_id(selected_project_id)
            new_task = selected_project.create_child()
            new_task.name = "New Task"
            self.view._task_list_frame.add_task_row(new_task)
            self.view._detail_frame._name_label["text"] = new_task.name # testcode