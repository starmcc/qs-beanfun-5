from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class TaskQueue(QObject):
    taskSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.taskQueue = []
        self.taskSignal.connect(self.processTask)

    def addTask(self, task, *args):
        self.taskQueue.append((task, args))
        if len(self.taskQueue) == 1:
            self.taskSignal.emit(self.taskQueue[0])

    @pyqtSlot(object)
    def processTask(self, task_args):
        task, args = task_args
        task(*args)
        self.taskQueue.pop(0)
        if self.taskQueue:
            self.taskSignal.emit(self.taskQueue[0])
