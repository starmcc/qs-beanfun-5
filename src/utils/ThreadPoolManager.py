import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Optional, Any, Dict

from PySide6.QtCore import QObject, Signal, QTimer, Qt
from PySide6.QtWidgets import QWidget

from src.components.LoadingTask import LoadingMask


class ThreadPoolManager(QObject):
    """
    线程池管理器 - 优化线程使用效率
    """
    # 任务完成信号
    task_finished = Signal(dict)

    def __init__(self, max_workers: int = 4, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="QsBeanfun")
        self._task_counter = 0
        self._active_tasks: Dict[str, Future] = {}
        self._loading_masks: Dict[str, LoadingMask] = {}
        self._lock = threading.Lock()

    def submit_task(self,
                    task_func: Callable,
                    callback_func: Optional[Callable] = None,
                    parent_win: Optional[QWidget] = None,
                    show_loading: bool = True,
                    task_name: Optional[str] = None,
                    *args, **kwargs) -> str:
        """
        提交任务到线程池

        Args:
            task_func: 要执行的任务函数
            callback_func: 任务完成后的回调函数
            parent_win: 父窗口
            show_loading: 是否显示加载遮罩
            task_name: 任务名称（用于调试）
            *args, **kwargs: 传递给任务函数的参数

        Returns:
            str: 任务ID
        """
        with self._lock:
            self._task_counter += 1
            task_id = f"task_{self._task_counter}_{int(time.time())}"

        # 创建包装函数，添加异常处理
        def wrapped_task():
            result = None
            exception = None
            try:
                result = task_func(*args, **kwargs)
            except Exception as e:
                exception = e
                logging.error(f"任务 {task_name or task_func.__name__} 执行异常: {str(e)}", exc_info=True)
            finally:
                # 发送完成信号
                self.task_finished.emit({
                    "task_id": task_id,
                    "parent": parent_win,
                    "result": result,
                    "exception": exception,
                    "callback": callback_func
                })

        # 提交任务到线程池
        future = self.executor.submit(wrapped_task)

        with self._lock:
            self._active_tasks[task_id] = future

        # 显示加载遮罩
        if show_loading and parent_win:
            load_mask = LoadingMask(parent_win)
            self._loading_masks[task_id] = load_mask
            QTimer.singleShot(0, load_mask.show)

        return task_id

    def _handle_task_finished(self, result_data: Dict[str, Any]) -> None:
        """处理任务完成"""
        task_id = result_data["task_id"]
        parent_win = result_data["parent"]
        result = result_data["result"]
        exception = result_data["exception"]
        callback_func = result_data["callback"]

        # 清理加载遮罩
        if task_id in self._loading_masks:
            load_mask = self._loading_masks.pop(task_id)
            QTimer.singleShot(0, lambda: (load_mask.hide(), load_mask.deleteLater()))

        # 清理任务记录
        with self._lock:
            self._active_tasks.pop(task_id, None)

        # 执行回调
        if callback_func is not None:
            try:
                callback_func(parent_win, result, exception)
            except Exception as e:
                logging.error(f"回调函数执行异常: {str(e)}", exc_info=True)

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self._lock:
            future = self._active_tasks.get(task_id)
            if future:
                success = future.cancel()
                if success:
                    self._active_tasks.pop(task_id, None)
                    # 清理加载遮罩
                    if task_id in self._loading_masks:
                        load_mask = self._loading_masks.pop(task_id)
                        QTimer.singleShot(0, lambda: (load_mask.hide(), load_mask.deleteLater()))
                return success
        return False

    def get_active_task_count(self) -> int:
        """获取活跃任务数量"""
        with self._lock:
            return len(self._active_tasks)

    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池"""
        # 取消所有未完成的任务
        with self._lock:
            for future in self._active_tasks.values():
                future.cancel()
            self._active_tasks.clear()

        # 关闭线程池
        self.executor.shutdown(wait=wait)

        # 清理加载遮罩
        for load_mask in self._loading_masks.values():
            QTimer.singleShot(0, lambda m=load_mask: (m.hide(), m.deleteLater()))
        self._loading_masks.clear()


# 全局线程池实例
_thread_pool_manager: Optional[ThreadPoolManager] = None
_lock = threading.Lock()


def get_thread_pool() -> ThreadPoolManager:
    """获取全局线程池实例（单例模式）"""
    global _thread_pool_manager
    if _thread_pool_manager is None:
        with _lock:
            if _thread_pool_manager is None:
                _thread_pool_manager = ThreadPoolManager(max_workers=4)
                # 连接信号，Qt6 QueuedConnection 枚举不变
                _thread_pool_manager.task_finished.connect(_thread_pool_manager._handle_task_finished,
                                                           Qt.ConnectionType.QueuedConnection)
    return _thread_pool_manager


def shutdown_thread_pool() -> None:
    """关闭全局线程池"""
    global _thread_pool_manager
    if _thread_pool_manager is not None:
        with _lock:
            if _thread_pool_manager is not None:
                _thread_pool_manager.shutdown()
                _thread_pool_manager = None
