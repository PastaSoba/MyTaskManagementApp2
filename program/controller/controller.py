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
        self.view._project_list_frame._project_treeview.bind("<<TreeviewSelect>>", self.__on_project_treeview_select)

        self.__construct_initial_view() # 初期状態のビューを構築

    def __construct_initial_view(self):
        """初期状態のビューを構築する
        """
        # プロジェクト一覧とタスク一覧を取得
        projects = self.model.get_children()
        # view._project_list_frameにプロジェクト一覧を表示
        self.view._project_list_frame.add_project_rows(projects)
        # view._task_list_frameに最初のプロジェクトのタスク一覧を表示
        if len(projects) > 0:
            self.view._task_list_frame.add_task_rows(projects[0].get_children())

    def __on_project_treeview_select(self, event):
        """プロジェクト一覧のTreeViewで行が選択された際の処理

        1. 選択されたプロジェクトのタスク一覧を取得
        2. view._task_list_frameのタスク一覧表示を更新
        """
        selected_project_id = UUID(self.view._project_list_frame._project_treeview.selection()[0])
        selected_project = self.model.get_child_by_id(selected_project_id)
        self.view._task_list_frame.delete_all_task_rows()
        self.view._task_list_frame.add_task_rows(selected_project.get_children())