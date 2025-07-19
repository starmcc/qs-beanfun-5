import re
from abc import abstractmethod

from src.config.GlobalConfig import *
from src.models import Account, ActInfoResult
from src.models.LoginRecord import LoginRecord


class QsClient:

    @abstractmethod
    def login(self, act: str, pwd: str) -> LoginRecord:
        pass

    @abstractmethod
    def login_return_token(self, login_record: LoginRecord) -> LoginRecord:
        pass

    @abstractmethod
    def get_account_list(self, bf_web_token: str) -> ActInfoResult:
        pass

    @abstractmethod
    def get_session_key(self) -> (bool, str):
        pass

    @abstractmethod
    def __get_act_create_time(self, sn: str):
        pass

    @abstractmethod
    def add_account(self, new_name: str) -> (bool, str):
        pass

    @abstractmethod
    def change_account_name(self, account_id: str, new_name: str) -> (bool, str):
        pass

    @abstractmethod
    def get_dynamic_password(self, account: Account, bf_web_token: str):
        pass

    @abstractmethod
    def get_web_url_member_center(self, bf_web_token: str) -> str:
        pass

    @abstractmethod
    def get_web_url_service_center(self) -> str:
        pass

    @abstractmethod
    def get_web_url_user_recharge(self, bf_web_token: str) -> str:
        pass

    @abstractmethod
    def get_web_url_register(self) -> str:
        pass

    @abstractmethod
    def get_web_url_forgot_pwd(self) -> str:
        pass

    @abstractmethod
    def heartbeat(self):
        pass

    @abstractmethod
    def login_out(self):
        pass

    @abstractmethod
    def dual_very_login(self, login_result: LoginRecord) -> LoginRecord:
        pass

    @abstractmethod
    def get_game_points(self, bf_web_token: str) -> int:
        pass

    def regex_login_request_params(self, text: str) -> (str, str, str):
        data_list = re.findall(r'id="__VIEWSTATE"\svalue="(.*?)"\s/>', text)
        viewstate = data_list[0] if data_list else None
        data_list = re.findall(r'id="__EVENTVALIDATION"\svalue="(.*?)"\s/>', text)
        eventvalidation = data_list[0] if data_list else None
        data_list = re.findall(r'id="__VIEWSTATEGENERATOR"\svalue="(.*?)"\s/>', text)
        viewstateGenerator = data_list[0] if data_list else None
        return viewstate, eventvalidation, viewstateGenerator

    def result_json_handler(self, rsp, msg) -> (bool, str):
        # 检查HTTP响应状态码
        if rsp.status_code != 200:
            return False, f'请求失败，状态码: {rsp.status_code}'
        try:
            # 解析JSON响应
            entry = rsp.json()
        except ValueError as e:
            return False, f'JSON解析失败: {str(e)}'
        # 检查响应数据结构完整性
        if not isinstance(entry, dict):
            return False, f'{msg}失败(1)!'
        # 获取intResult字段并验证
        int_result = entry.get('intResult')
        if int_result is None:
            return False, f'{msg}失败(2)!'
        # 检查业务逻辑状态码
        if int_result != 1:
            return False, entry.get('strOutstring', f'{msg}失败!')
        # 处理成功
        return True, f'{msg}成功!'


def get_instance() -> QsClient:
    if GLOBAL_CONFIG.now_login_type == GLOBAL_ACT_TYPE_TW:
        from src.client.impl.TwClientImpl import TwClientImpl
        return TwClientImpl()
    from src.client.impl.HkClientImpl import HkClientImpl
    return HkClientImpl()
