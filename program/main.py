from model.model import ProjectRoot
from view.view import MainWindow
from controller.controller import Controller



def main():
    model = ProjectRoot.load()
    view  = MainWindow()
    controller = Controller(model, view)
    view.window.mainloop()

if __name__ == "__main__":
    main()