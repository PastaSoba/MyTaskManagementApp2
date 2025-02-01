import flet as ft
from model.model import Project

class ProjectListFrame:
    def __init__(self):
        # fletのColumnでレイアウト
        self.view = ft.Column(expand=True)
        # プロジェクト一覧はListViewで表現
        self.project_list = ft.ListView(expand=True, spacing=10)
        self.add_project_button = ft.FilledButton(text="+ Add Project")
        self.view.controls.extend([self.project_list, self.add_project_button])

    def get_view(self):
        return self.view

    def add_project_row(self, project: Project):
        # ListTileでプロジェクト行を追加
        project_tile = ft.ListTile(
            title=ft.Text(project.name, size=20, color="white"),
            id=str(project.id)
        )
        self.project_list.controls.append(project_tile)
        self.project_list.update()

    # ...必要に応じた他のメソッドも同様にflet用へ変更...