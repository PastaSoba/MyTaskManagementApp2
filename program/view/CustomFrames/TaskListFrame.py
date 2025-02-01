import flet as ft
from model.model import Task

class TaskListFrame:
    def __init__(self):
        self.view = ft.Column(expand=True)
        self.task_list = ft.ListView(expand=True, spacing=10)
        self.add_task_button = ft.FilledButton(text="+ Add Task")
        self.view.controls.extend([self.task_list, self.add_task_button])

    def get_view(self):
        return self.view

    def add_task_row(self, task: Task, parent: str = ""):
        # カード形式でタスク情報を表示
        task_card = ft.Card(
            content=ft.Column([
                ft.Text(task.name, size=18, color="white"),
                ft.Text(task.due.isoformat(), size=14, color="white"),
                ft.Text(task.status.value, size=14, color="white")
            ], tight=True)
        )
        self.task_list.controls.append(task_card)
        self.task_list.update()

    # ... add_task_rows, update_task_row, delete_all_task_rows も同様に...