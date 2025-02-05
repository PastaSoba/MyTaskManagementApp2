import flet as ft
from view.CustomContainer.ProjectListContainer import ProjectListContainer
from view.CustomContainer.TaskListColumn import TaskListColumn
from view.CustomContainer.DetailColumn import DetailColumn



class MainWindow():
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.DARK
        self.project_list_container :ProjectListContainer = ProjectListContainer()
        self.task_list_column    :TaskListColumn    = TaskListColumn()
        self.detail_column       :DetailColumn      = DetailColumn()

        # width ratio of columns
        self.project_list_container.column.expand = 1
        self.task_list_column.column.expand = 2
        self.detail_column.column.expand = 2

        self.page.add(
            ft.Row([
                self.project_list_container,
                self.task_list_column.column,
                self.detail_column.column
            ], expand=True)
        )
        self.page.update()
