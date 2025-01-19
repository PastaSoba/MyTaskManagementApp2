from enum import Enum

class TaskStatus(Enum):
    """
    タスクのステータスの列挙型。

    Atrributes
    ----------
    TODO : str
        まだ開始されていないタスクを表します。
    PROGRESS : str
        現在進行中のタスクを表します。
    DONE : str
        完了したタスクを表します。
    """
    TODO = "TODO"
    PROGRESS = "PROGRESS"
    DONE = "DONE"
