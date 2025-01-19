from model.model import Task, TaskStatus, Priority, Project, ProjectRoot
from view.view import MainWindow
from pprint import pprint



def main():
    view = MainWindow()
    view.window.mainloop()

if __name__ == "__main__":
    main()