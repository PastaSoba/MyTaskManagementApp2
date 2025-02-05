import flet as ft
from model.model import Project



class ListTileWithId(ft.ListTile):
    def __init__(self, id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id


class ProjectListFrame:
    def __init__(self):
        self.view = ft.Column(expand=True)
        self.project_list = ft.ListView(expand=True, spacing=10)
        self.add_project_button = ft.FilledTonalButton(text="+ Add Project")
        self.view.controls.extend([self.project_list, self.add_project_button])

    def get_view(self):
        return self.view

    def add_project_row(self, project: Project):
        """プロジェクト情報を表示する行を追加する

        Args:
            project (Project): プロジェクト情報
        """
        project_tile = ListTileWithId(
            id=str(project.id),
            title=ft.Text(project.name, size=20, color="white")
        )
        self.project_list.controls.append(project_tile)
        # self.project_list.update()

    def add_project_rows(self, projects: list[Project]):
        """プロジェクト情報を複数行追加する

        Args:
            projects (list[Project]): プロジェクト情報のリスト
        """
        for project in projects:
            self.add_project_row(project)
        self.project_list.update()

    # ...必要に応じた他のメソッドも同様にflet用へ変更...