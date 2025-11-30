import logging
import os
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

# 确保正确加载qrc资源，防止Pycharm误删
# noinspection PyUnresolvedReferences
import src.Resources_rc
from src import LoggingConfig
from src.utils import BaseTools, BoxPop, ThreadPoolManager
from src.window.LoginWin import LoginWin

def on_app_about_to_quit():
    ThreadPoolManager.shutdown_thread_pool()
    logging.info("线程池已销毁")

class QsBeanfun(QApplication):
    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except ValueError as ve:
            if "Data must be aligned to block boundary in ECB mode" in str(ve):
                logging.error("加密解密数据出现对齐问题！")
                return False
            else:
                self._handle_exception(ve)
                return False
        except Exception as e:
            self._handle_exception(e)
            return False

    def _handle_exception(self, e):
        logging.error("捕获到未处理的异常", exc_info=True)

# -------------------------- 主程序入口 --------------------------
if __name__ == '__main__':
    LoggingConfig.setup_logging()
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    try:
        chrome_path = BaseTools.build_chrome()
        if chrome_path:
            os.environ["QTWEBENGINEPROCESS_PATH"] = chrome_path
        else:
            logging.warning("未找到chrome.exe, QTWebEngine可能无法正常加载加速器")
    except Exception as e:
        logging.error(f"file chrome.exe build error {str(e)}")

    app = QsBeanfun(sys.argv)
    app.aboutToQuit.connect(on_app_about_to_quit)

    win_login = LoginWin()
    if BaseTools.check_cn_path(os.getcwd()):
        BoxPop.show_message_box(win_login, "目中存在汉字,无法运行", f"存放程序的文件夹目录有汉字\n请删掉汉字后运行！", QMessageBox.Warning)
        sys.exit(1)
    win_login.show()
    logging.info(f"启动完成")
    sys.exit(app.exec_())