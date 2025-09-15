import logging
from typing import Callable, Optional, Any, Dict

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QObject, Qt
from PyQt5.QtWidgets import QWidget

from src.window.LoadingTask import LoadingMask


class CustomThread(QThread):
    finished = pyqtSignal(dict)

    def __init__(self,
                 task_func: Optional[Callable] = None,
                 parent: Optional[QObject] = None,
                 *args, **kwargs):
        super().__init__()
        self.task_func = task_func  # 任务函数
        self.parent = parent
        self.args = args  # 任务函数位置参数
        self.kwargs = kwargs  # 任务函数关键字参数
        self._result: Any = None  # 任务执行结果
        self._exception: Optional[Exception] = None  # 捕获的异常

    def run(self) -> None:
        """线程执行入口，执行任务并捕获异常"""
        try:
            if self.task_func is not None:
                self._result = self.task_func(*self.args, **self.kwargs)
        except Exception as e:
            self._exception = e
            logging.error(f"线程任务执行异常: {str(e)}", exc_info=True)  # 详细异常日志
        finally:
            # 发送完整结果信息
            self.finished.emit({
                "parent": self.parent,
                "result": self._result,
                "exception": self._exception
            })

    @staticmethod
    def run_task(task_func: Callable,
                 callback_func: Optional[Callable] = None,
                 parent_win: Optional[QWidget] = None,
                 show_loading: bool = True,
                 *args, **kwargs) -> 'CustomThread':
        """
        启动线程执行任务的静态方法
        参数:
            task_func: 要在子线程执行的任务函数
            callback_func: 任务完成后的回调函数，接收(self, result, exception)参数
            parent_win: 父窗口
            show_loading: 是否显示加载遮罩
            *args, **kwargs: 传递给任务函数的参数
        """
        # 创建线程实例，指定父对象便于资源管理
        thread = CustomThread(
            task_func=task_func,
            parent=parent_win,
            *args, **kwargs
        )

        # 加载遮罩管理
        load_mask = None
        if show_loading and parent_win:
            load_mask = LoadingMask(parent_win)
            # 确保在主线程显示遮罩
            QTimer.singleShot(0, load_mask.show)

        def handle_finished(result_data: Dict[str, Any]) -> None:
            """处理线程结束逻辑：清理资源、调用回调"""
            # 确保加载遮罩在主线程关闭并释放
            if load_mask is not None:
                QTimer.singleShot(0, lambda: (load_mask.hide(), load_mask.deleteLater()))

            # 提取结果数据
            if callback_func is not None:
                try:
                    callback_func(result_data["parent"], result_data["result"], result_data["exception"])
                except Exception as e:
                    logging.error(f"回调函数执行异常: {str(e)}", exc_info=True)
            # 线程资源清理
            thread.deleteLater()

        # 连接信号与槽（使用QueuedConnection确保主线程执行）
        thread.finished.connect(handle_finished, Qt.QueuedConnection)
        # 线程结束后自动退出事件循环
        thread.finished.connect(thread.quit)

        # 启动线程
        thread.start()
        return thread
