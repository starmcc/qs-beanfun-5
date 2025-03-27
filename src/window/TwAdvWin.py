import re
import time

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog

from src.client import RequestClient
from src.utils import BaseTools, BoxPop
from src.views.Ui_TwAdv import Ui_TwAdv


class TwAdvWin(QDialog, Ui_TwAdv):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.samplecaptcha = ''
        self.viewstate = ''
        self.eventvalidation = ''
        self.viewstateGenerator = ''
        self.setupUi(self)
        BaseTools.set_basic_window(self)
        self.init_ui()

    def init_ui(self):
        self.label_verifyCode.mousePressEvent = self.load_verify_image
        self.pushButton_send.clicked.connect(self.continue_login)
        self.open_advance_check()

    def open_advance_check(self):
        rsp = RequestClient.get_instance().get('https://tw.newlogin.beanfun.com/LoginCheck/AdvanceCheck.aspx')
        data_list = re.findall(r'id="__VIEWSTATE"\svalue="(.*?)"\s/>', rsp.text)
        self.viewstate = data_list[0] if data_list else None
        data_list = re.findall(r'id="__EVENTVALIDATION"\svalue="(.*?)"\s/>', rsp.text)
        self.eventvalidation = data_list[0] if data_list else None
        data_list = re.findall(r'id="__VIEWSTATEGENERATOR"\svalue="(.*?)"\s/>', rsp.text)
        self.viewstateGenerator = data_list[0] if data_list else None
        data_list = re.findall(r'id="LBD_VCID_c_logincheck_advancecheck_samplecaptcha" value="(.*)"', rsp.text)
        self.samplecaptcha = data_list[0] if data_list else None
        data_list = re.findall(r'<span id="lblAuthType">(.*)</span>', rsp.text)
        self.label_tips.setText(data_list[0] if data_list else '')
        self.load_verify_image()

    def load_verify_image(self, event=None):
        # 请求验证码图片
        params = {
            'get': 'image',
            'c': 'c_logincheck_advancecheck_samplecaptcha',
            't': self.samplecaptcha,
            'd': time.time() * 1000
        }
        rsp = RequestClient.get_instance().get('https://tw.newlogin.beanfun.com/LoginCheck/BotDetectCaptcha.ashx', params=params)
        # 先将二进制数据转换为QImage对象
        image = QImage.fromData(rsp.content)
        # 再从QImage对象转换得到QPixmap对象
        pixmap = QPixmap.fromImage(image)
        self.label_verifyCode.setPixmap(pixmap)

    def continue_login(self):
        if not self.lineEdit_phone.text():
            BoxPop.err(self, '请输入手机号码!')
            return

        if not self.lineEdit_verifyCode.text():
            BoxPop.err(self, '请输入验证码!')
            self.load_verify_image()
            return

        data = {
            '__VIEWSTATE': self.viewstate,
            '__EVENTVALIDATION': self.eventvalidation,
            '__VIEWSTATEGENERATOR': self.viewstateGenerator,
            'txtVerify': self.lineEdit_phone.text().strip(),
            'CodeTextBox': self.lineEdit_verifyCode.text().strip(),
            'imgbtnSubmit.x': '73',
            'imgbtnSubmit.y': '23',
            'LBD_VCID_c_logincheck_advancecheck_samplecaptcha': self.samplecaptcha,
        }
        rsp = RequestClient.get_instance().post('https://tw.newlogin.beanfun.com/LoginCheck/AdvanceCheck.aspx', data=data)
        if rsp.status_code != 200:
            BoxPop.err(self, '网络错误')
            return

        data_list = re.findall(r'<span id="lblMessage" style="color:Red;">(.*?)</span>', rsp.text)
        err_msg = data_list[0] if data_list else None
        # 有错误消息，返回
        if err_msg:
            BoxPop.err(self, err_msg)
            self.load_verify_image()
            return

        data_list = re.findall(r"alert\('([^']*)'\)", rsp.text)
        msg = data_list[0] if data_list else None
        if not msg:
            BoxPop.err(self, '未知错误,无法获得Beanfun信息!')
            return
        BoxPop.info(self, msg)
        self.close()
