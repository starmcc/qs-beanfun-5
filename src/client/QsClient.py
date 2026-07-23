import json
import logging
import re
from abc import abstractmethod
from typing import Tuple

from src.client import RequestClient
from src.config.GlobalConfig import *
from src.models import Account, ActInfoResult
from src.models.LoginRecord import LoginRecord


class QsClient:

    @abstractmethod
    def get_login_index(self) -> str:
        pass

    @abstractmethod
    def login(self, act: str, pwd: str,
              check_token=None,
              login_token=None) -> LoginRecord:
        pass

    @abstractmethod
    def login_return_token(self, login_record: LoginRecord) -> LoginRecord:
        pass

    @abstractmethod
    def get_account_list(self, bf_web_token: str) -> ActInfoResult:
        pass

    def get_session_key(self) -> Tuple[bool, str]:
        url = ''
        if GLOBAL_CONFIG.now_login_type == ActType.TW.value:
            url = 'https://tw.beanfun.com/beanfun_block/bflogin/default.aspx'
        else:
            url = "https://bfweb.hk.beanfun.com/beanfun_block/bflogin/default.aspx"
        params = {'service': '999999_T0'}
        response = RequestClient.get_instance().get(url, params=params)
        if response.status_code != 200:
            return False, '登入失败,请检查网络环境[0]'
        redirect_urls = [r.url for r in response.history]
        for url in redirect_urls:
            match = re.search(r'skey=([\w]+)', str(url))
            if match:
                return True, match.group(1)
        result_text = response.text.encode('iso-8859-1').decode('utf-8')
        if "IP已自動被系統鎖定" in result_text:
            return False, '登入频繁,IP已自动被官方锁定,请检查网络环境'
        return False, f'登入失败,请检查网络环境\n{result_text}'

    @abstractmethod
    def __get_act_create_time(self, sn: str):
        pass

    @abstractmethod
    def add_account(self, new_name: str) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def change_account_name(self, account_id: str, new_name: str) -> Tuple[bool, str]:
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

    def get_classic_data(self, bf_web_token: str) -> dict:
        """获取经典版(怀旧服)登录数据，返回包含 UserObjectID 和 UserSessionToken 的字典"""
        # 第一步：GET 获取 OTT
        url = 'https://galaxy.games.gamania.com/webapi/view/login/mstc?redirect_url=https://maplestoryclassic.beanfun.com/Main?af_click_id='
        rsp = RequestClient.get_instance().get(url)
        if rsp.status_code != 200:
            logging.error(f'获取经典版OTT失败，状态码: {rsp.status_code}')
            return None
        pat1 = r'var ott = "([^"]+)"'
        match_obj = re.search(pat1, rsp.text)
        if not match_obj:
            logging.error('获取经典版OTT失败，未匹配到ott值')
            return None
        ott_value = match_obj.group(1)
        logging.info(f'提取到OTT: {ott_value}')

        # 第二步：POST 获取登录结果
        params = {
            "ott": ott_value,
            "fromSelf": True
        }
        url = f'https://galaxy.games.gamania.com/webapi/view/login/result/mstc/ghk?WebToken={bf_web_token}'
        rsp = RequestClient.get_instance().post(url, params=params)
        if rsp.status_code != 200:
            logging.error(f'获取经典版数据失败，状态码: {rsp.status_code}')
            return None
        try:
            j = json.loads(rsp.text)
        except ValueError as e:
            logging.error(f'获取经典版数据JSON解析失败: {str(e)}')
            return None
        status = j.get('Status', {})
        if status.get('Code') != 0:
            logging.error(f'获取经典版数据失败，Status.Code: {status.get("Code")}')
            return None
        results = j.get('Results', {})
        if not results:
            logging.error('获取经典版数据失败，Results为空')
            return None
        logging.info(f'获取经典版数据成功，UserObjectID: {results.get("UserObjectID")}')
        return {
            'UserObjectID': results.get('UserObjectID'),
            'UserSessionToken': results.get('UserSessionToken'),
        }

    def regex_login_request_params(self, text: str) -> Tuple[str, str, str]:
        data_list = re.findall(r'id="__VIEWSTATE"\svalue="(.*?)"\s/>', text)
        viewstate = data_list[0] if data_list else None
        data_list = re.findall(r'id="__EVENTVALIDATION"\svalue="(.*?)"\s/>', text)
        eventvalidation = data_list[0] if data_list else None
        data_list = re.findall(r'id="__VIEWSTATEGENERATOR"\svalue="(.*?)"\s/>', text)
        viewstateGenerator = data_list[0] if data_list else None
        return viewstate, eventvalidation, viewstateGenerator

    def result_json_handler(self, rsp, msg) -> Tuple[bool, str]:
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
    if GLOBAL_CONFIG.now_login_type == ActType.TW.value:
        from src.client.impl.TwClientImpl import TwClientImpl
        return TwClientImpl()
    from src.client.impl.HkClientImpl import HkClientImpl
    return HkClientImpl()
