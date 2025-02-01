import flet as ft
from view.configs import Config
from view.CustomFrames.DetailFrame import ProjectDetailFrame  # または TaskDetailFrame
from view.CustomFrames.TaskListFrame import TaskListFrame
from view.CustomFrames.ProjectListFrame import ProjectListFrame

def main(page: ft.Page):
    page.title = Config.WINDOW_TITLE
    page.window_width = 1000
    page.window_height = 600

    # fletではPanedWindowの代わりにRowやColumnで画面構成
    project_list_frame = ProjectListFrame()
    task_list_frame = TaskListFrame()
    detail_frame = ProjectDetailFrame()  # 表示する内容に応じて選択

    page.add(
        ft.Row([
            project_list_frame.get_view(),
            task_list_frame.get_view(),
            detail_frame.get_view()
        ], expand=True)
    )

ft.app(target=main)

