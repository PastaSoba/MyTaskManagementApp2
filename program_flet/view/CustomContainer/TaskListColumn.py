import flet as ft


class TaskListColumn:
    def __init__(self):
        self._column = ft.Column()
        self.task_list = ft.ListView(expand=True, spacing=10)
        self.add_task_button = ft.FilledButton(text="+ Add Task")
        self._column.controls.extend([self.task_list, self.add_task_button])

    @property
    def column(self) -> ft.Column:
        return self._column