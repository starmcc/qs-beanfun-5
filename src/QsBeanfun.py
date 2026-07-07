import logging
import os
import sys

import urllib3
from PySide6.QtWidgets import QApplication, QMessageBox

# 确保正确加载qrc资源，防止Pycharm误删
# noinspection PyUnresolvedReferences
import src.Resources_rc
from src import LoggingConfig
from src.utils import BaseTools, BoxPop
from src.window.LoginWin import LoginWin


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
    # 原有屏蔽系统深色代码保留
    os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        chrome_path = BaseTools.build_chrome()
        if chrome_path:
            os.environ["QTWEBENGINEPROCESS_PATH"] = chrome_path
        else:
            logging.warning("未找到chrome.exe, QTWebEngine可能无法正常加载加速器")
    except Exception as e:
        logging.error(f"file chrome.exe build error {str(e)}")

    app = QsBeanfun(sys.argv)

    win_login = LoginWin()
    if BaseTools.check_cn_path(os.getcwd()):
        BoxPop.show_message_box(win_login,
                                "目录中存在汉字,无法运行",
                                f"存放程序的文件夹目录有汉字\n请删掉汉字后运行！",
                                QMessageBox.Icon.Warning)
        sys.exit(1)
    win_login.show()
    logging.info(f"启动完成")
    sys.exit(app.exec())
