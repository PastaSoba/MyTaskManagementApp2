import flet as ft
from model.model import Project
from view.CustomComponent.CustomComponent import *




class ProjectListContainer(ft.Container):
    def __init__(self):
        super().__init__(bgcolor=ft.Colors.BLUE_300, expand=True)

        self.column = ft.Column(expand=True)
        self.project_list = ft.ListView(expand=True)
        self.add_project_button = ft.FilledTonalButton(text="+ Add Project")
        self.column.controls.extend([self.project_list, self.add_project_button])

        self.content = self.column


    def add_project_row(self, project: Project):
        """プロジェクト情報を表示する行を追加する

        Args:
            project (Project): プロジェクト情報
        """
        project_row = TextButtonWithId(
            id=str(project.id),
            text=project.name, icon=ft.Icons.BOOK)
        self.project_list.controls.append(project_row)
        self.update()

    def add_project_rows(self, projects: list[Project]):
        for project in projects:
            self.add_project_row(project)