import flet as ft


class DetailColumn:
    def __init__(self):
        self._column = ft.Column()
    
    @property
    def column(self) -> ft.Column:
        return self._column