import flet as ft

class LabeledEntry:
    def __init__(self, label_value: str = ""):
        self.container = ft.Column(controls=[
            ft.Text(label_value),
            ft.TextField()
        ])
    def get_view(self):
        return self.container
    def set(self, value: str):
        self.container.controls[1].value = value
        self.container.controls[1].update()
    def get(self) -> str:
        return self.container.controls[1].value

class LabeledText:
    def __init__(self, label_value: str = ""):
        self.container = ft.Column(controls=[
            ft.Text(label_value),
            ft.TextField(multiline=True, expand=True)
        ])
    def get_view(self):
        return self.container
    def set(self, value: str):
        self.container.controls[1].value = value
        self.container.controls[1].update()
    def get(self) -> str:
        return self.container.controls[1].value

class LabeledCombobox:
    def __init__(self, label_value: str = "", options: list[str] = None):
        self.container = ft.Column(controls=[
            ft.Text(label_value),
            ft.Dropdown(options=[ft.dropdown.Option(opt) for opt in (options or [])])
        ])
    def get_view(self):
        return self.container
    def set(self, value: str):
        dropdown = self.container.controls[1]
        dropdown.value = value
        dropdown.update()
    def get(self) -> str:
        return self.container.controls[1].value