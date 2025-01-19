import tkinter as tk
import tkinter.ttk as ttk

from view.configs import Config
from view.CustomFrames.DetailFrame import DetailFrame
from view.CustomFrames.TaskListFrame import TaskListFrame
from view.CustomFrames.ProjectListFrame import ProjectListFrame



class MainWindow:
    def __init__(self):
        # ウィンドウの初期化
        self.window = tk.Tk()
        self.window.title(Config.WINDOW_TITLE)
        self.window.geometry(Config.INITIAL_WINDOW_SIZE)


        self._paned_window       = tk.PanedWindow(self.window, orient=tk.HORIZONTAL)
        self._project_list_frame = ProjectListFrame(self._paned_window)
        self._task_list_frame    = TaskListFrame(self._paned_window)
        self._detail_frame       = DetailFrame(self._paned_window)



        self._paned_window.pack(fill=tk.BOTH, expand=True)
        self._paned_window.add(self._project_list_frame.frame)
        self._paned_window.add(self._task_list_frame.frame   )
        self._paned_window.add(self._detail_frame.frame      )

