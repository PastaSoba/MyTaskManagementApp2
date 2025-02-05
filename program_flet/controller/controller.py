from model.model import *
from view.view import *


class Controller:
    ######### シングルトン ########
    _instance = None
    def __new__(cls, model:ProjectRoot, view:MainWindow):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    ###############################


    def __init__(self, model: ProjectRoot, view: MainWindow):
        self.model = model
        self.view = view

        self.__construct_initial_view()

    def __construct_initial_view(self):
        """初期状態のビューを構築する"""
        projects = self.model.get_children()
        self.view.project_list_container.add_project_rows(projects)

        