import flet as ft
from model.model import ProjectRoot
from view.view import MainWindow
from controller.controller import Controller



def main(page: ft.Page):
    model = ProjectRoot.load()
    view  = MainWindow(page)
    controller = Controller(model, view)

if __name__ == "__main__":
    ft.app(main)