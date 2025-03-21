import logging
import sys
import traceback
from logging.handlers import TimedRotatingFileHandler
from PyQt5.QtWidgets import QApplication

# 确保正确加载qrc资源，防止Pycharm误删
import src.Resources_rc
from src.utils import BaseTools
from src.window.LoginWin import LoginWin


class QsBeanfun(QApplication):

    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except ValueError as ve:
            if "Data must be aligned to block boundary in ECB mode" in str(ve):
                # 这里可以弹出提示框告知用户加密解密数据对齐问题等友好提示信息
                print("加密解密数据出现对齐问题，请检查相关数据！")
                return False
            else:
                self._handle_exception(ve)
                return False
        except Exception as e:
            self._handle_exception(e)
            return False

    def _handle_exception(self, e):
        logger = logging.getLogger(__name__)
        logger.error("捕获到异常", exc_info=True)
        traceback.print_exc()


if __name__ == '__main__':
    # 配置日志文件处理器
    timed_rotating_file_handler = TimedRotatingFileHandler(
        BaseTools.build_path('app.log'), when='w0', backupCount=4
    )
    # 配置控制台日志处理器
    console_handler = logging.StreamHandler(sys.stdout)

    logging_config = {
        'format': '%(asctime)s | %(levelname)s:  %(message)s | %(filename)s : %(module)s : %(lineno)d',
        'datefmt': '%Y-%m-%d %H:%M:%S',
        'level': logging.INFO,  # root logger的级别设置为INFO
        'handlers': [timed_rotating_file_handler, console_handler],
    }
    logging.basicConfig(**logging_config)

    app = QsBeanfun(sys.argv)
    win_login = LoginWin()
    sys.exit(app.exec_())
