import time
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
# 启动调度任务
scheduler.start()


def do_task(func: Callable, milliseconds: int = 200, attr=None):
    global scheduler
    # 添加调度任务，调度方法为 timedtask，触发器选择 interval（间隔性），间隔时长为 2 秒
    task_id = func.__name__ + str(time.time())
    scheduler.add_job(func, 'interval', seconds=milliseconds / 1000, id=task_id,
                      args=(task_id, attr) if attr else (task_id,))
    return task_id


def stop_task(task_id: str):
    global scheduler
    scheduler.remove_job(task_id)
