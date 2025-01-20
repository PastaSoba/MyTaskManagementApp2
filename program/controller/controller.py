from uuid import UUID

from model.model import ProjectRoot
from view.view import MainWindow



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

        1. 選択されたタスクの詳細をview._detail_frameに表示
        2. view._detail_frameの表示を更新   
        """
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
        self.view._detail_frame._name_label["text"] = new_project.name