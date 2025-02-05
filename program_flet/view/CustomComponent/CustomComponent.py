import flet as ft





class TextButtonWithId(ft.TextButton):
    """識別子(id)を持つTextButton
    """
    def __init__(self, id: str, **kwargs):
        super().__init__(**kwargs)
        self.id = id