import datetime
import html
import logging
import re
import time
from typing import Tuple

from src.client import RequestClient
from src.client.QsClient import QsClient
from src.models.Account import Account
from src.models.ActInfoResult import ActInfoResult
from src.models.LoginRecord import LoginRecord
from src.models.TwResponseJson import TwResponseJson
from src.utils import De2Utils


class TwClientImpl(QsClient):

    def get_login_index(self) -> str:
        return "https://tw.beanfun.com/beanfun_block/bflogin/default.aspx?service=999999_T0"

    def login(self, act: str, pwd: str) -> LoginRecord:
        RequestClient.get_instance().client.cookies.clear()
        login_record = LoginRecord(status=False, message='')

        ok, session_key = self.get_session_key()

        if not ok:
            login_record.message = session_key
            return login_record
        login_record.skey = session_key
        params = {
            'pSKey': login_record.skey
        }
        rsp = RequestClient.get_instance().get('https://login.beanfun.com/Login/Index', params=params)
        if rsp.status_code != 200:
            login_record.message = session_key
            return login_record
        result = re.search(r'<input name="__RequestVerificationToken".*?value="([^"]+?)"', rsp.text)
        # 取出 token
        login_record.requestVerificationToken = result.group(1)
        if not login_record.requestVerificationToken:
            login_record.message = 'requestVerificationToken获取失败[1]'
            return login_record

        rsp = RequestClient.get_instance().get('https://login.beanfun.com/Login/InitLogin')
        if rsp.status_code != 200:
            login_record.message = f"HTTP请求失败，状态码：{rsp.status_code}"
            return login_record
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'referer': f'https://login.beanfun.com/Login/Index?pSKey={login_record.skey}',
            'RequestVerificationToken': login_record.requestVerificationToken,
        }
        url = 'https://login.beanfun.com/Login/CheckAccountType'
        json = {'Account': act}
        rsp = RequestClient.get_instance().post(url, json=json, headers=headers)
        if rsp.status_code != 200:
            login_record.message = f"HTTP请求失败，状态码：{rsp.status_code}"
            return login_record
        jsonEntry = TwResponseJson.from_response(rsp)
        if jsonEntry.ResultCode != 1:
            login_record.message = jsonEntry.ResultMessage
            return login_record
        else:
            if jsonEntry.ResultData.get('IsGamaPass'):
                login_record.message = '请使用GamePass登入,登入器使用官网登入即可!'
                return login_record

        url = "https://login.beanfun.com/Login/AccountLogin"
        json = {
            'Account': act,
            'Pasw': pwd,
            'IsMobile': False,
        }
        rsp = RequestClient.get_instance().post(url, headers=headers, json=json)
        jsonEntry = TwResponseJson.from_response(rsp)
        if jsonEntry.ResultCode == 0:
            login_record.message = jsonEntry.ResultMessage
            return login_record
        elif jsonEntry.ResultCode == 2:
            if jsonEntry.ResultMessage == "AccountLock":
                login_record.message = '您的帳號已被鎖定,可聯繫客服人員了解原因'
                return login_record
            else:
                if jsonEntry.Result == 2:
                    login_record.message = '請先進行遊戲點數補繳後才能解除鎖定'
                    return login_record
                else:
                    # ====================== adv验证 ======================
                    login_record.status = True
                    login_record.adv_status = True
                    # 这里获取的是服务端返回的验证地址
                    login_record.location = jsonEntry.ResultMessage
                    return login_record
                    # ====================== adv验证End ======================

        url = "https://login.beanfun.com/Login/SendLogin"

        headers = {
            'Referer': f'https://login.beanfun.com/Login/Index?pSKey={session_key}'
        }
        rsp = RequestClient.get_instance().get(url, headers=headers)
        login_record.content = rsp.text

        return self.login_return_token(login_record)

    def login_return_token(self, login_record: LoginRecord) -> LoginRecord:
        payload = {}
        input_tags = re.findall(r'<input[^>]+>', login_record.content, re.IGNORECASE)
        for tag in input_tags:
            tag_str = tag
            # 匹配 name value 属性
            name_match = re.search(r'name\s*=\s*[\'\"]([^\'\"]+)[\'\"]', tag_str, re.IGNORECASE)
            val_match = re.search(r'value\s*=\s*[\'\"]([^\'\"]*)[\'\"]', tag_str, re.IGNORECASE)
            if name_match and val_match and "type=\"submit\"" not in tag_str.lower():
                name = name_match.group(1)
                value = val_match.group(1)
                payload[name] = value

        if len(payload) == 0:
            login_record.message = '登录失败'
            return login_record
        headers = {
            'Referer': 'https://login.beanfun.com/'
        }
        rsp = RequestClient.get_instance().post("https://tw.beanfun.com/beanfun_block/bflogin/return.aspx",
                                                data=payload, headers=headers, allow_redirects=False)

        set_cookie_header = rsp.headers.get("Set-Cookie", "")
        match = re.search(r"bfWebToken=([^;]+)", set_cookie_header)
        login_record.bfWebToken = match.group(1) if match else None
        if login_record.bfWebToken is None or login_record.bfWebToken == '':
            login_record.message = '登入失败,请检查网络环境[3]'
            return login_record
        login_record.status = True
        login_record.message = '登录成功!'
        return login_record

    def get_account_list(self, bf_web_token: str) -> ActInfoResult:
        actResult = ActInfoResult()
        url = "https://tw.beanfun.com/beanfun_block/auth.aspx"
        params = {
            'channel': 'game_zone',
            'page_and_query': 'game_start.aspx?service_code_and_region=610074_T9',
            'web_token': bf_web_token,
        }
        rsp = RequestClient.get_instance().get(url, params=params)
        text = html.unescape(rsp.text)

        if rsp.status_code != 200:
            return actResult
        data_list = re.findall(r'onclick="([^"]*)"><div id="(\w+)" sn="(\d+)" name="([^"]+)"', text)
        if not data_list:
            # 进阶认证校验
            data_list = re.findall(
                r'<div\sid="divServiceAccountAmountLimitNotice"\sclass="InnerContent">(.*)</div>', text)
            certStr = data_list[0] if data_list else None
            if certStr.find("進階認證") >= 0:
                # 没有做进阶认证
                actResult.cert_status = False
            if re.search(r'<div\sid="divServiceInstruction">請先創立新帳戶</div>', text):
                # 新账号，没有账号
                actResult.new_user = True

            # 检查是否已经做了进阶认证
            actResult.auth_cert = re.search(r'm_strMabiStatus\s=\s"0"', text)

            return actResult
        actResult.accounts = []
        for item in data_list:
            account = Account()
            account.status = (item[0] != "")
            account.id = item[1]
            account.sn = item[2]
            account.name = item[3]
            account.create_time = self.__get_act_create_time(account.sn)
            actResult.accounts.append(account)
        return actResult

    def __get_act_create_time(self, sn: str):
        url = "https://tw.beanfun.com/beanfun_block/game_zone/game_start_step2.aspx"
        now = datetime.datetime.now()
        str_date_time = f"{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}{now.minute}"
        params = {
            'service_code': '610074',
            'service_region': 'T9',
            'sotp': sn,
            'dt': str_date_time,
        }
        rsp = RequestClient.get_instance().get(url, params=params)
        if rsp.status_code != 200:
            return None
        dataList = re.findall(r'ServiceAccountCreateTime:\s"([^"]+)"', rsp.text)
        return dataList[0] if dataList else None

    def add_account(self, new_name: str) -> Tuple[bool, str]:
        url = 'https://tw.beanfun.com/generic_handlers/gamezone.ashx'
        data = {
            'strFunction': 'AddServiceAccount',
            'npsc': '',
            'npsr': '',
            'sc': '610074',
            'sr': 'T9',
            'sadn': new_name.strip(),
            'sag': '',
        }
        rsp = RequestClient.get_instance().post(url, data=data, timeout=60)
        return self.result_json_handler(rsp, '创建')

    def change_account_name(self, account_id: str, new_name: str) -> Tuple[bool, str]:
        url = "https://tw.beanfun.com/generic_handlers/gamezone.ashx"
        data = {
            'strFunction': 'ChangeServiceAccountDisplayName',
            'sl': '610074_T9',
            'said': account_id,
            'nsadn': new_name.strip(),
        }
        rsp = RequestClient.get_instance().post(url, data=data)
        return self.result_json_handler(rsp, '修改')

    def get_dynamic_password(self, account: Account, bf_web_token: str):
        if account is None or account.id is None or account.id.strip() == "":
            return None
        url = "https://tw.beanfun.com/beanfun_block/game_zone/game_start_step2.aspx"
        params = {
            'service_code': '610074',
            'service_region': 'T9',
            'sotp': account.sn,
            'dt': f"{datetime.date.today().year}{datetime.date.today().month}{datetime.date.today().day}{datetime.datetime.now().hour}{datetime.datetime.now().minute}{datetime.datetime.now().second}{datetime.datetime.now().minute}"
        }
        rsp = RequestClient.get_instance().get(url, params=params)

        if rsp.status_code != 200:
            return None
        dataList = re.findall('GetResultByLongPolling&key=(.*?)"', rsp.text)
        pollingKey = dataList[0] if dataList else None
        if not account.create_time:
            dataList = re.findall(r'ServiceAccountCreateTime:\s"([^"]+)"', rsp.text)
            account.create_time = dataList[0] if dataList else None

        url = "https://tw.newlogin.beanfun.com/generic_handlers/get_cookies.ashx"
        rsp = RequestClient.get_instance().get(url)
        if rsp.status_code != 200:
            return None

        dataList = re.findall(r"var\sm_strSecretCode\s=\s'(.*)'", rsp.text)
        secret = dataList[0] if dataList else None

        url = "https://tw.beanfun.com/beanfun_block/generic_handlers/record_service_start.ashx"
        data = {
            'service_code': '610074',
            'service_region': 'T9',
            'service_account_id': account.id,
            'sotp': account.sn,
            'service_account_display_name': account.name,
            'service_account_create_time': account.create_time,
        }
        rsp = RequestClient.get_instance().post(url, data=data)
        if rsp.status_code != 200:
            return None

        url = "https://tw.beanfun.com/beanfun_block/generic_handlers/get_webstart_otp.ashx"
        params = {
            'sn': pollingKey,
            'WebToken': bf_web_token,
            'SecretCode': secret,
            'ppppp': 'F9B45415B9321DB9635028EFDBDDB44B4012B05F95865CB8909B2C851CFE1EE11CB784F32E4347AB7001A763100D90768D8A4E30BCC3E80C',
            'ServiceCode': '610074',
            'ServiceRegion': 'T9',
            'ServiceAccount': account.id,
            'CreateTime': account.create_time,
            'd': time.time() * 1000
        }
        rsp = RequestClient.get_instance().get(url, params=params)
        if rsp.status_code != 200:
            return None
        return De2Utils.decrypt_des_no_pkcs_hex(rsp.text)

    def get_web_url_member_center(self, bf_web_token: str) -> str:
        return 'https://tw.beanfun.com/TW/auth.aspx?channel=member&page_and_query=default.aspx%3Fservice_code%3D999999%26service_region%3DT0&web_token=' + bf_web_token

    def get_web_url_service_center(self) -> str:
        return 'https://tw.beanfun.com/customerservice/www/main.aspx'

    def get_web_url_user_recharge(self, bf_web_token: str) -> str:
        return 'https://tw.beanfun.com/TW/auth.aspx?channel=gash&page_and_query=default.aspx%3Fservice_code%3D999999%26service_region%3DT0&web_token=' + bf_web_token

    def get_web_url_register(self) -> str:
        time = datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')[:-3]
        return 'https://bfweb.beanfun.com/Register/register?isbfApp=0&service=999999_T0&dt=' + time

    def get_web_url_forgot_pwd(self) -> str:
        return 'https://tw.beanfun.com/member/forgot_pwd.aspx'

    def heartbeat(self):
        rsp = RequestClient.get_instance().get(
            'https://tw.beanfun.com/beanfun_block/generic_handlers/echo_token.ashx?webtoken=1')
        logging.info(f'heartbeat')

    def login_out(self):
        RequestClient.get_instance().get(
            f'https://tw.beanfun.com/generic_handlers/remove_bflogin_session.ashx?d={int(time.time() * 1000)}')

    def dual_very_login(self, login_result: LoginRecord) -> LoginRecord:
        pass

    def get_game_points(self, bf_web_token: str) -> int:
        url = 'https://tw.beanfun.com/beanfun_block/generic_handlers/get_remain_point.ashx'
        params = {
            'noCacheIE': datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3],
            'webtoken': "1"
        }
        rsp = RequestClient.get_instance().get(url, params=params)
        if rsp.status_code != 200:
            return 0
        data_list = re.findall(r'"RemainPoint"\s:\s"(\d+)"', rsp.text)
        points = data_list[0] if data_list else None
        if not points:
            return 0
        try:
            return int(points)
        except Exception as e:
            logging.error(f"发生错误:\n{str(e)}")
            return 0

    def regex_login_request_params(self, text: str) -> Tuple[str, str, str]:
        return super().regex_login_request_params(text)

    def result_json_handler(self, rsp, msg) -> Tuple[bool, str]:
        return super().result_json_handler(rsp, msg)
