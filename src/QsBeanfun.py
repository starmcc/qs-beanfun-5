import logging
import os
import sys

from PyQt5.QtWidgets import QApplication

# 确保正确加载qrc资源，防止Pycharm误删
# noinspection PyUnresolvedReferences
import src.Resources_rc
from src.utils import BaseTools
from src.window.LoginWin import LoginWin


class QsBeanfun(QApplication):

    def notify(self, receiver, event):
        try:
            return super().notify(receiver, event)
        except ValueError as ve:
            if "Data must be aligned to block boundary in ECB mode" in str(ve):
                logging.error("加密解密数据出现对齐问题，请检查相关数据！")
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


if __name__ == '__main__':
    # 配置日志文件处理器
    file_handler = logging.FileHandler(BaseTools.build_path('app.log'), encoding='utf-8')
    # 配置控制台日志处理器
    console_handler = logging.StreamHandler(sys.stdout)
    logging_config = {
        'format': '%(asctime)s | %(levelname)s:  %(message)s | %(filename)s : %(module)s : %(lineno)d',
        'datefmt': '%Y-%m-%d %H:%M:%S',
        'level': logging.INFO,
        'handlers': [file_handler, console_handler],
    }
    logging.basicConfig(**logging_config)

    # 禁止缩放
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    try:
        # 构建QtWebEngineProcess的复制品chrome.exe 适配加速器
        chrome_path = BaseTools.build_chrome()
        if chrome_path:
            # 设置QtWebEngineProcess的环境变量让其读取chrome.exe
            os.environ["QTWEBENGINEPROCESS_PATH"] = chrome_path
    except Exception as e:
        logging.error(f"file chrome.exe build error {e}")

    app = QsBeanfun(sys.argv)
    win_login = LoginWin()
    win_login.show()
    sys.exit(app.exec_())
