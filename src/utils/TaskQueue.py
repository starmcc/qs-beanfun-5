import logging

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class TaskQueue(QObject):
    taskSignal = pyqtSignal(object)  # 信号传递任务信息

    def __init__(self):
        super().__init__()
        self.taskQueue = []  # 任务队列存储格式: [(task, args, kwargs), ...]
        self.taskSignal.connect(self.processTask)  # 连接信号与处理函数

    def addTask(self, task, *args, **kwargs):
        """添加任务到队列，支持位置参数和关键字参数"""
        # 将任务、位置参数、关键字参数一起存入队列
        self.taskQueue.append((task, args, kwargs))

        # 如果是第一个任务，立即触发处理
        if len(self.taskQueue) == 1:
            self.taskSignal.emit(self.taskQueue[0])

    @pyqtSlot(object)
    def processTask(self, task_info):
        """处理任务，执行后自动调度下一个任务"""
        task, args, kwargs = task_info
        try:
            # 同时传递位置参数和关键字参数
            task(*args, **kwargs)
        except Exception as e:
            logging.error(f"任务执行出错: {str(e)}")

        # 移除已完成的任务
        self.taskQueue.pop(0)

        # 如果还有任务，继续处理下一个
        if self.taskQueue:
            self.taskSignal.emit(self.taskQueue[0])
