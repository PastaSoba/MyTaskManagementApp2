import flet as ft
from view.configs import Config
from view.CustomFrames.DetailFrame import ProjectDetailFrame  # または TaskDetailFrame
from view.CustomFrames.TaskListFrame import TaskListFrame
from view.CustomFrames.ProjectListFrame import ProjectListFrame


class MainWindow:
    def __init__(self):
        ft.app(target=self.main)

    def main(self, page: ft.Page):
        page.title = Config.WINDOW_TITLE


        # fletではPanedWindowの代わりにRowやColumnで画面構成
        self.project_list_frame = ProjectListFrame()
        self.task_list_frame = TaskListFrame()
        self.detail_frame = ProjectDetailFrame()  # 表示する内容に応じて選択

        page.add(
            ft.Row([
                self.project_list_frame.get_view(),
                self.task_list_frame.get_view(),
                self.detail_frame.get_view()
            ] , expand=True)
        )


