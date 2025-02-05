from enum import Enum

class Priority(Enum):
    """
    タスク管理の優先度レベル。

    Attributes
    ----------
    EMERGENCY_IMPORTANT : str
        "1: Emergency & Important for you"
    IMPORTANT : str
        "2: Important for you"
    EMERGENCY : str
        "3: Emergency"
    NOT_YOUR_JOB : str
        "4: Not your job"
    """
    EMERGENCY_IMPORTANT = "1: Emergency & Important for you"
    IMPORTANT = "2: Important for you"
    EMERGENCY = "3: Emergency"
    NOT_YOUR_JOB = "4: Not your job"
