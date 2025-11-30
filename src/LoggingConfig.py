import io
import logging
import sys

from src.utils import BaseTools


def setup_logging():
    """
    - 测试：级别=DEBUG
    - 生产：级别=INFO
    """
    is_production = getattr(sys, 'frozen', False)
    log_level = logging.INFO if is_production else logging.DEBUG

    root_logger = logging.getLogger()
    root_logger.handlers.clear()  # 清空原有处理器
    root_logger.setLevel(log_level)  # 设置根Logger级别

    log_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s:  %(message)s | %(filename)s : %(module)s : %(lineno)d',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(BaseTools.build_path('app.log'), encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    class ConsoleStream(io.StringIO):
        def write(self, msg):
            sys.__stdout__.write(msg)
            sys.__stdout__.flush()

    if sys.stdout != sys.__stdout__:
        sys.stdout = ConsoleStream()
        sys.stderr = ConsoleStream()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    env_tag = "生产" if is_production else "测试"
    logging.info(f"日志初始化完成 | 环境：{env_tag} | 级别：{logging.getLevelName(log_level)}")