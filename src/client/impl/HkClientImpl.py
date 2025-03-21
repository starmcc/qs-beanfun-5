import datetime
import html
import json
import logging
import re
import time

from src.client import RequestClient
from src.client.QsClient import QsClient
from src.models.Account import Account
from src.models.ActInfoResult import ActInfoResult
from src.models.LoginRecord import LoginRecord
from src.utils import DeUtils


class HkClientImpl(QsClient):

    def change_account_name(self, account_id: str, new_name: str) -> (bool, str):
        url = "https://bfweb.hk.beanfun.com/generic_handlers/gamezone.ashx"
        data = {
            'strFunction': 'ChangeServiceAccountDisplayName',
            'sl': '610074_T9',
            'said': account_id,
            'nsadn': new_name.strip(),
        }
        rsp = RequestClient.get_instance().post(url, data=data)
        if rsp.status_code != 200:
            return False, '请求失败!'
        entry = json.loads(rsp.text)
        if not entry or not entry.get('intResult'):
            return False, '解析失败!'
        if entry.get('intResult') == 1:
            return True, 'ok'
        return False, entry.get('strOutstring')

    def add_account(self, new_name: str) -> (bool, str):
        url = "https://bfweb.hk.beanfun.com/generic_handlers/gamezone.ashx"
        data = {
            'strFunction': 'AddServiceAccount',
            'npsc': '',
            'npsr': '',
            'sc': '610074',
            'sr': 'T9',
            'sadn': new_name.strip(),
            'sag': '',
        }
        rsp = RequestClient.get_instance().post(url, data=data)
        if rsp.status_code != 200:
            return False, '请求失败!'
        entry = json.loads(rsp.text)
        if not entry or not entry.get('intResult'):
            return False, '解析失败!'
        if entry.get('intResult') == 1:
            return True, 'ok'
        return False, entry.get('strOutstring')

    def login(self, act: str, pwd: str) -> LoginRecord:
        RequestClient.get_instance().client.cookies.jar.clear()
        login_record = LoginRecord(status=False, message='')

        ok, data = self.get_session_key()
        if not ok:
            login_record.message = data
            return login_record

        login_record.skey = data
        url = f"https://login.hk.beanfun.com/login/id-pass_form_newBF.aspx?otp1={login_record.skey}"
        rsp = RequestClient.get_instance().get(url)
        login_record.content = rsp.text
        viewstate, eventvalidation, viewstateGenerator = self.regex_login_request_params(login_record.content)

        if not viewstate or not eventvalidation or not viewstateGenerator:
            login_record.message = '无法获取关键参数\r[viewstate][eventvalidation][viewstateGenerator]'
            return login_record

        url = f"https://login.hk.beanfun.com/login/id-pass_form_newBF.aspx?otp1={login_record.skey}"

        data = {'__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATEENCRYPTED': '',
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                '__VIEWSTATEGENERATOR': viewstateGenerator,
                't_AccountID': act,
                't_Password': pwd,
                'token1': '',
                'g-recaptcha-response': '',
                'btn_login': '登入'}
        rsp = RequestClient.get_instance().post(url, data=data)
        login_record.content = rsp.text

        data_list = re.findall(r"<script>ShowMsgBox\('(.*?)'", login_record.content)
        err_msg = data_list[0] if data_list else None
        if err_msg:
            login_record.message = err_msg
            return login_record

        # ====================== 双重验证 ======================
        daul_status = re.search(r'請輸入雙重驗證碼', login_record.content)
        if daul_status:
            login_record.daul_status = True
            login_record.message = 'doubleVerify'
            return login_record
        # ====================== 双重验证End ======================

        data_list = re.findall(r'AuthKey\.value\s=\s"(.*?)";parent', login_record.content)
        login_record.auth_key = data_list[0] if data_list else None
        return self.login_return_token(login_record)

    def login_return_token(self, login_record: LoginRecord) -> LoginRecord:
        data = {
            'SessionKey': login_record.skey,
            'AuthKey': login_record.auth_key,
            'ServiceCode': '',
            'ServiceRegion': '',
            'ServiceAccountSN': '0',
        }
        rsp = RequestClient.get_instance().post('https://bfweb.hk.beanfun.com/beanfun_block/bflogin/return.aspx', data=data)
        login_record.content = rsp.text

        if rsp.status_code != 200:
            login_record.message = f'登录失败! Status code:{rsp.status_code}'
            return login_record

        # 获取token，如果没有则失败!
        login_record.bfWebToken = RequestClient.get_ck_val('bfWebToken')
        if not login_record.bfWebToken:
            login_record.message = '登录失败! bfWebToken is NULL!'
            return login_record

        login_record.status = True
        login_record.message = '登录成功!'
        return login_record

    def get_session_key(self) -> (bool, str):
        url = "https://bfweb.hk.beanfun.com/beanfun_block/bflogin/default.aspx"
        params = {'service': '999999_T0'}
        response = RequestClient.get_instance().get(url, params=params)
        if response.status_code != 200:
            return False, '获取sKey失败-1'
        if "已自動被系統鎖定" in response.text:
            return False, "IP已自動被系統鎖定"
        if "目前無法在您的國家或地區瀏覽此網站" in response.text:
            return False, "目前無法在您的國家或地區瀏覽此網站"
        redirect_urls = [r.url for r in response.history]
        for url in redirect_urls:
            match = re.search(r'skey=([\w]+)', str(url))
            if match:
                return True, match.group(1)
        return False, '获取sKey失败-2'

    def get_account_list(self, bf_web_token: str) -> ActInfoResult:
        actResult = ActInfoResult()
        url = "https://bfweb.hk.beanfun.com/beanfun_block/auth.aspx"
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
        url = "https://bfweb.hk.beanfun.com/beanfun_block/game_zone/game_start_step2.aspx"
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

    def get_dynamic_password(self, account: Account, bf_web_token: str):
        if account is None or account.id is None or account.id.strip() == "":
            return None
        url = "https://bfweb.hk.beanfun.com/beanfun_block/game_zone/game_start_step2.aspx"
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

        url = "https://login.hk.beanfun.com/generic_handlers/get_cookies.ashx"
        rsp = RequestClient.get_instance().get(url)
        if rsp.status_code != 200:
            return None

        dataList = re.findall(r"var\sm_strSecretCode\s=\s'(.*)'", rsp.text)
        secret = dataList[0] if dataList else None

        url = "https://bfweb.hk.beanfun.com/beanfun_block/generic_handlers/record_service_start.ashx"
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

        url = "https://bfweb.hk.beanfun.com/beanfun_block/generic_handlers/get_webstart_otp.ashx"
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
        return DeUtils.decrypt_des_no_pkcs_hex(rsp.text)

    def get_web_url_member_center(self, bf_web_token) -> str:
        return f"https://bfweb.hk.beanfun.com/HK/auth.aspx?channel=member&page_and_query=default.aspx%3Fservice_code%3D999999%26service_region%3DT0&web_token={bf_web_token}"

    def get_web_url_service_center(self) -> str:
        return 'https://csp.hk.beanfun.com/'

    def get_web_url_user_recharge(self, bf_web_token: str) -> str:
        return f"https://bfweb.hk.beanfun.com/HK/auth.aspx?channel=gash&page_and_query=default.aspx%3Fservice_code%3D999999%26service_region%3DT0&web_token={bf_web_token}"

    def get_web_url_register(self) -> str:
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]
        return f"https://bfweb.hk.beanfun.com/beanfun_web_ap/signup/default.aspx?service=999999_T0&dt={now_time}"

    def get_web_url_forgot_pwd(self) -> str:
        return "https://bfweb.hk.beanfun.com/member/forgot_pwd.aspx"

    def heartbeat(self):
        rsp = RequestClient.get_instance().get('https://bfweb.hk.beanfun.com/')
        logging.info(f'heartbeat')

    def login_out(self):
        RequestClient.get_instance().get(
            f'https://bfweb.hk.beanfun.com/generic_handlers/remove_bflogin_session.ashx?d={int(time.time() * 1000)}')

    def dual_very_login(self, login_record: LoginRecord) -> LoginRecord:
        """
            双重验证登录，参数与普通登录不一样哦
        """
        login_record.daul_status = False
        viewstate, eventvalidation, viewstateGenerator = self.regex_login_request_params(login_record.content)
        data = {'__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATEENCRYPTED': '',
                '__VIEWSTATE': viewstate,
                '__EVENTVALIDATION': eventvalidation,
                '__VIEWSTATEGENERATOR': viewstateGenerator,
                'token1': '',
                'totpLoginBtn': '登入'}
        if not viewstate or not eventvalidation or not viewstateGenerator:
            login_record.message = '无法获取关键参数[viewstate][eventvalidation][viewstateGenerator]'
            return login_record
        for index, char in enumerate(login_record.dual_code):
            data[f'otpCode{index + 1}'] = char
        rsp = RequestClient.get_instance().post(
            f"https://login.hk.beanfun.com/login/id-pass_form_newBF.aspx?otp1={login_record.skey}", data=data)
        login_record.content = rsp.text
        data_list = re.findall(r"<script>ShowMsgBox\('(.*?)'", login_record.content)
        err_msg = data_list[0] if data_list else None
        if err_msg:
            # 错误消息 设置True外层继续循环
            login_record.daul_status = True
            login_record.message = err_msg
            return login_record

        data_list = re.findall(r'AuthKey\.value\s=\s\"(.*?)\";parent', login_record.content)
        if not data_list:
            login_record.message = '双重验证获取AuthKey失败!'
            return login_record

        login_record.authkey = data_list[0]

        # 呼叫接口 该接口用于设置cookies bfUID bfTD
        data_list = re.findall(r'var\sstrWriteUrl\s=\s"(.*)";', login_record.content)
        handle_write_cookie_url = data_list[0] if data_list else None
        if not handle_write_cookie_url:
            login_record.message = '呼叫失败!'
            return login_record
        rsp = RequestClient.get_instance().get(handle_write_cookie_url)
        json_val = json.loads(rsp.text)
        if not json_val or json_val.get('Result') != 1:
            login_record.message = '呼叫失败2!'
            return login_record

        return self.login_return_token(login_record)

    def get_game_points(self, bf_web_token: str) -> int:
        url = 'https://bfweb.hk.beanfun.com/beanfun_block/generic_handlers/get_remain_point.ashx'
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
            logging.error(e)
            return 0

    def regex_login_request_params(self, text: str) -> (str, str, str):
        return super().regex_login_request_params(text)
