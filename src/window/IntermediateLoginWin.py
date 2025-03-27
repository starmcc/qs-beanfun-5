import json
import logging
import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from src.client import RequestClient, QsClient
from src.models.LoginRecord import LoginRecord
from src.utils import BaseTools, SchedulerManager
from src.views.Ui_IntermediateLogin import Ui_IntermediateLogin


class IntermediateLoginWin(QDialog, Ui_IntermediateLogin):
    data_sent = pyqtSignal(LoginRecord)
    close_signal = pyqtSignal()
    # 最大等待秒數
    MAX_AWAIT_SECONDS = 60 * 3

    def __init__(self, parent=None, login_record: LoginRecord = None):
        super().__init__(parent)
        self.login_record: LoginRecord = login_record
        self.setupUi(self)
        BaseTools.set_basic_window(self)
        self.await_num = 0
        self.close_signal.connect(self.handle_close)
        self.task_id = SchedulerManager.do_task(self.polling_login, 1000)

    def polling_login(self, task_id):
        self.await_num += 1
        self.label_await.setText(f'等待App确认登录\n请在{self.MAX_AWAIT_SECONDS - self.await_num}秒内进行操作!')

        status, self.login_record.auth_key = self.intermediate_login()
        self.login_record.intermediate_login = False
        self.login_record.status = False
        if status == 2:
            self.login_record = QsClient.get_instance().login_return_token(self.login_record)
        elif self.await_num > self.MAX_AWAIT_SECONDS:
            self.login_record.message = '已超时,请重新登录!'
        else:
            return
        self.task_id = -1
        SchedulerManager.stop_task(task_id)
        self.close_signal.emit()

    def handle_close(self):
        self.close()
    def closeEvent(self, event):
        # 如果直接關閉窗口，需要手動停止任務，不然會一直執行
        if self.task_id != -1:
            SchedulerManager.stop_task(self.task_id)
        self.data_sent.emit(self.login_record)
        super().closeEvent(event)

    def intermediate_login(self) -> (int, str):
        akey = ''
        try:
            # 开始轮询请求获取登录状态
            rsp = RequestClient.get_instance().post('https://tw.newlogin.beanfun.com/login/bfAPPAutoLogin.ashx', data={'lt': self.login_record.lt})
            if rsp.status_code != 200:
                return -1, akey
            entry = json.loads(rsp.text)
            int_result = entry.get('IntResult')
            if not entry or not int_result:
                return int_result, akey
            if int_result != 2:
                return int_result, akey
            rsp = RequestClient.get_instance().get('https://tw.newlogin.beanfun.com/login/' + entry.get('StrReslut'))
            if rsp.status_code != 200:
                return int_result, akey
            data_list = re.findall(r'AuthKey\.value\s=\s"(.*?)";parent', rsp.text)
            akey = data_list[0] if data_list else ''
            return int_result, akey
        except Exception as e:
            logging.error(e)
            return -500, akey
