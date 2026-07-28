import logging
import math
from decimal import Decimal
from typing import Tuple

from PySide6.QtCore import QEvent
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtWidgets import QWidget

from src.client import QsClient
from src.config import Config
from src.config.GlobalConfig import GLOBAL_CONFIG, ActType
from src.models.Account import Account
from src.models.ActInfoResult import ActInfoResult
from src.utils import BaseTools, SystemCom, BoxPop, SchedulerManager, WinManager
from src.utils.ThreadPoolManager import get_thread_pool
from src.views.Ui_Main import Ui_Main
from src.window import CustomToolTipWin
from src.window.ConfigWin import ConfigWin
from src.components.TrayIcon import TrayIcon


class MainWin(QWidget, Ui_Main):
    trayIcon: TrayIcon
    nowAccount: Account = Account()
    # 怀旧服数据
    classic_result = {}
    task_id: str

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        WinManager.set_basic_window(self)
        self.children_accounts: list[Account] = []
        self.auth_cert = True
        self.init_ui()
        self.get_account_info()
        # 定时心跳保证登录状态
        self.task_id = SchedulerManager.do_task(self.refresh_login_status, 1000 * 60 * 5)

    def closeEvent(self, a0):
        # 当窗口关闭时停止心跳
        SchedulerManager.stop_task(self.task_id)
        self.trayIcon.deleteLater()
        super().closeEvent(a0)

    @staticmethod
    def refresh_login_status(task_id):
        QsClient.get_instance().heartbeat()

    def init_ui(self):
        self.trayIcon = TrayIcon(self)
        # 设置图片
        self.label_logoView.setPixmap(QPixmap(":/images/banner"))
        self.checkBox_autoInput.setChecked(Config.auto_input())
        self.pushButton_dynamicPwd.clicked.connect(self.dynamicPwd_clicked)
        self.pushButton_start.clicked.connect(self.start_clicked)
        self.pushButton_classic.clicked.connect(self.classic_clicked)
        self.pushButton_config.clicked.connect(self.config_clicked)
        self.pushButton_createAct.clicked.connect(self.createAct_clicked)
        self.pushButton_loginOut.clicked.connect(self.user_loginOut_triggerd)
        self.lineEdit_numAct.installEventFilter(self)  # 安装事件过滤器
        self.lineEdit_dynamicPwd.installEventFilter(self)
        self.checkBox_autoInput.stateChanged.connect(self.autoInput_stateChanged)
        self.comboBox_gameAct.currentIndexChanged.connect(self.refresh_account_info)
        self.label_points.mousePressEvent = self.refresh_points
        self.label_status.mousePressEvent = self.get_account_info
        CustomToolTipWin.build_tips(self, self.label_points, "账户拥有的储值点数")
        CustomToolTipWin.build_tips(self, self.label_status,
                                    "如显示封禁请立刻联系官方客服解除!\n菜单 -> 用户中心 -> 客服中心 -> 联系客服 -> 填写信息并等待客服邮件回复\n建议勿使用外挂/辅助/宏/VPN等软件\n官方一经查实永久封禁,误封可解除")
        CustomToolTipWin.build_tips(self, self.checkBox_autoInput,
                                    f"勾选后点击{self.pushButton_dynamicPwd.text()}将自动聚焦《新枫之谷》\n并自动在游戏中输入数字账号和动态密令")
        # 经典版按钮：台湾 GamaPass 登录 或 香港登录 时显示
        is_classic_visible = (
            (GLOBAL_CONFIG.now_login_type == ActType.TW.value and GLOBAL_CONFIG.is_gamapass_login)
            or GLOBAL_CONFIG.now_login_type == ActType.HK.value
        )
        self.pushButton_classic.setVisible(is_classic_visible)
        self.pushButton_loginOut.setFocus()

    def eventFilter(self, obj, event):
        # Qt6 事件类型枚举无需修改判断逻辑，event.type() 兼容
        if obj == self.lineEdit_numAct:
            if event.type() == QEvent.Type.HoverEnter:
                self.lineEdit_numAct.setText(self.nowAccount.id)
            elif event.type() == QEvent.Type.HoverLeave:
                self.lineEdit_numAct.setText(BaseTools.hidden_str(self.nowAccount.id))
        elif obj == self.lineEdit_dynamicPwd:
            if event.type() == QEvent.Type.HoverEnter:
                self.lineEdit_dynamicPwd.setText(self.nowAccount.dynamic_pwd)
            elif event.type() == QEvent.Type.HoverLeave:
                self.lineEdit_dynamicPwd.setText(BaseTools.hidden_str(self.nowAccount.dynamic_pwd))

        return super().eventFilter(obj, event)

    def createAct_clicked(self):
        if not self.auth_cert:
            BoxPop.info(self, '此账号尚未完成进阶认证,请前往会员中心完成后【重新登录】!')
            return
        text, ok = BoxPop.input_dialog(self, '新建账号', '请输入账号昵称')
        if not ok or not text:
            return

        def __task():
            return QsClient.get_instance().add_account(text)

        def __result(win, args: Tuple[bool, str], e):
            if not args:
                args = (False, "未知错误!")
            status, msg = args
            if e:
                msg = "添加账号异常!"
            if status:
                BoxPop.info(win, msg)
                win.get_account_info()
            else:
                BoxPop.err(win, msg)

        get_thread_pool().submit_task(__task, __result, self, True)

    def autoInput_stateChanged(self):
        Config.auto_input(self.checkBox_autoInput.isChecked())

    def dynamicPwd_clicked(self):
        def __task(win):
            win.get_dynamic_password()
            if not win.nowAccount.dynamic_pwd:
                return False
            return True

        def __result(win, status, e):
            if e or not status:
                BoxPop.err(win, "获取动态密令失败")
                return
            try:
                # 需要运行游戏才能执行自动输入
                if win.checkBox_autoInput.isChecked() and SystemCom.check_game_running():
                    status, msg = SystemCom.auto_input_act_pwd(win.nowAccount.id, win.nowAccount.dynamic_pwd)
                    if status != 0:
                        BoxPop.err(win, msg)
            except Exception as e:
                logging.error(f"发生错误:\n{str(e)}")
                BoxPop.err(win, '自动输入失败,请手动复制输入!')

        get_thread_pool().submit_task(__task, __result, self, True, win=self)

    def start_clicked(self):
        def __task(win):
            if Config.pass_input():
                win.get_dynamic_password()
                if not win.nowAccount.dynamic_pwd:
                    return False
            return True

        def __result(win, status, e):
            if e or not status:
                BoxPop.err(win, "获取动态密令失败")
                return
            try:
                SystemCom.run_game(self, win.nowAccount.id, win.nowAccount.dynamic_pwd)
            except Exception as e:
                logging.error(f"发生错误:\n{str(e)}")
                BoxPop.err(win, f'启动游戏出现了问题:\n {str(e)}')

        get_thread_pool().submit_task(__task, __result, self, True, win=self)

    def classic_clicked(self):
        def __task(win):
            win.get_classic_login_data()
            return True

        def __result(win, status, e):
            if e or not status:
                BoxPop.err(win, "获取登录数据失败")
                return
            try:
                SystemCom.run_game_classic(self, win.classic_result['UserObjectID'], win.classic_result['UserSessionToken'])
            except Exception as e:
                logging.error(f"发生错误:\n{str(e)}")
                BoxPop.err(win, f'启动经典版游戏出现了问题:\n {str(e)}')

        get_thread_pool().submit_task(__task, __result, self, True, win=self)

    def get_classic_login_data(self):
        self.classic_result = QsClient.get_instance().get_classic_data(GLOBAL_CONFIG.bf_web_token)

    def get_dynamic_password(self):
        pwd = QsClient.get_instance().get_dynamic_password(self.nowAccount, GLOBAL_CONFIG.bf_web_token)
        pwd = pwd if pwd else None
        self.nowAccount.dynamic_pwd = pwd
        self.lineEdit_dynamicPwd.setText(BaseTools.hidden_str(pwd))

    def get_account_info(self, event=None):
        def __task():
            return QsClient.get_instance().get_account_list(GLOBAL_CONFIG.bf_web_token)

        def __result(win, actInfoResult: ActInfoResult, e):
            if e or not actInfoResult:
                BoxPop.err(win, '获取账号信息失败!')
                return
            win.children_accounts = actInfoResult.accounts
            win.auth_cert = actInfoResult.auth_cert
            win.comboBox_gameAct.clear()
            win.pushButton_createAct.setVisible(actInfoResult.new_user)
            win.pushButton_dynamicPwd.setEnabled(not actInfoResult.new_user)
            win.lineEdit_numAct.setText('')
            win.lineEdit_dynamicPwd.setText('')
            if actInfoResult.new_user is True or len(win.children_accounts) == 0:
                # 新账号
                if not win.auth_cert:
                    BoxPop.info(win, '此账号尚未完成电话进阶认证\n请前往会员中心完成后重新登录！')
                    # 不允许创建账号和查看账号详情
                    win.pushButton_createAct.setEnabled(False)
                return
            for entry in win.children_accounts:
                win.comboBox_gameAct.addItem(entry.name, userData=entry.id)
            win.comboBox_gameAct.setCurrentIndex(0)
            win.nowAccount = win.children_accounts[0]
            win.refresh_account_info(0)

        get_thread_pool().submit_task(__task, __result, self, True)

    def refresh_account_info(self, index):
        """
        刷新账号信息
        """
        item = self.comboBox_gameAct.itemData(index)
        for i, entry in enumerate(self.children_accounts):
            # 清空动态密码
            entry.dynamic_pwd = ''
            if entry.id == item:
                self.nowAccount = entry
                break
            if i == len(self.children_accounts) - 1:
                return
        palette = self.label_status.palette()
        if self.nowAccount.status:
            self.label_status.setText('正常')
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        else:
            self.label_status.setText('封禁')
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 0, 0))
        self.label_status.setPalette(palette)
        self.lineEdit_numAct.setText(BaseTools.hidden_str(self.nowAccount.id))
        self.lineEdit_dynamicPwd.setText('')
        self.refresh_points()

    def config_clicked(self):
        GLOBAL_CONFIG.win_config = ConfigWin(self)
        GLOBAL_CONFIG.win_config.exec()

    def refresh_points(self, event=None):
        def __task():
            points = QsClient.get_instance().get_game_points(GLOBAL_CONFIG.bf_web_token)
            points_game = math.floor(Decimal(points) / Decimal('2.5'))
            return f"{points}[{points_game}]"

        def __result(win, template: str, e):
            if e or not template:
                template = "0"
            win.label_points.setText(template)

        get_thread_pool().submit_task(__task, __result, self, True)

    def user_loginOut_triggerd(self):
        from src.window.LoginWin import LoginWin
        QsClient.get_instance().login_out()
        win_login = LoginWin()
        win_login.show()
        self.close()
