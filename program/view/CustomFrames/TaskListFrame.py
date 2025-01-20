import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional
from model.model import Task




class TaskListFrame:
    def __init__(self, parent):
        self.frame           : ttk.Frame           = ttk.Frame(parent)
        self._task_treeview  : Optional[ttk.Treeview] = None
        self._add_task_button: Optional[ttk.Button]   = None


        self.frame.pack(fill=tk.BOTH, expand=True)
        self.__create_task_treeview()
        self.__create_add_task_button()


    def __create_task_treeview(self):
        """タスク一覧を表示するTreeviewを作成して、frameに配置する
        """
        self._task_treeview = ttk.Treeview(
            self.frame,
            columns=["name"],
            show="tree headings",
        )
        self._task_treeview.heading("name", text="Task Name")
        self._task_treeview.column("#0", width=20, stretch=False)  # ツリー列の幅を設定
        self._task_treeview.column("name", width=200)
        self._task_treeview.pack(side=tk.TOP, fill="both", expand=True)

    def __create_add_task_button(self):
        """タスク追加ボタンを作成して、frameに配置する
        """
        self._add_task_button = ttk.Button(self.frame, text="+ Add Task")
        self._add_task_button.pack(side=tk.BOTTOM, fill="x")

    def add_task_row(self, task: Task, _parent=""):
        """タスク一覧を表示するTreeViewにタスクを表す行を追加する
        """
        # treeview中の行も、task.idで識別できるようにしてある
        self._task_treeview.insert(_parent, "end", iid=task.id, values=(task.name,))
        for child_task in task.get_children():
            self.add_task_row(child_task, _parent=task.id)

    def add_task_rows(self, tasks: list[Task]):
        """タスク一覧を表示するTreeViewに複数のタスクを表す行を追加する
        """
        for task in tasks:
            self.add_task_row(task)

    def delete_all_task_rows(self):
        """タスク一覧を表示するTreeViewの全アイテムを削除する"""
        self._task_treeview.delete(*self._task_treeview.get_children())