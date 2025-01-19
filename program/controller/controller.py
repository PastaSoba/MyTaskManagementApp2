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

        for project in self.model.get_children():
            self.view._project_list_frame.add_project_row(project)
        for task in self.model.get_children()[0].get_children():
            self.view._task_list_frame.add_task_row(task)