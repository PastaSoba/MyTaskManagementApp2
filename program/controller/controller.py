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
        self.__construct_initial_view()

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

    def set_callback(tk_obj, event_name: str, callback_func):
        """tkinterオブジェクトにイベントハンドラを設定する

        Parameters
        ----------
        tk_obj : tkinter.Widget
            イベントハンドラを設定する対象のtkオブジェクト
        event_name : str
            イベント名（例: <Button-1>）
        callback_func : Callable
            イベントハンドラとして設定する関数
        """
        tk_obj.bind(event_name, callback_func)