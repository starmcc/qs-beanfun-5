import datetime
import html
import json
import logging
import re
import time
from typing import Tuple

import config.Config
from config import Config
from config.GlobalConfig import GLOBAL_CONFIG
from src.client import RequestClient
from src.client.QsClient import QsClient
from src.models.Account import Account
from src.models.ActInfoResult import ActInfoResult
from src.models.LoginRecord import LoginRecord
from src.models.TwResponseJson import TwResponseJson
from src.utils import De2Utils
from src.utils import SystemCom


class TwClientImpl(QsClient):

    def get_login_index(self) -> str:
        return "https://tw.beanfun.com/beanfun_block/bflogin/default.aspx?service=999999_T0"

    def login(self, act: str, pwd: str,
              check_token=None,
              login_token=None) -> LoginRecord:
        RequestClient.get_instance().client.cookies.clear()
        login_record = LoginRecord(status=False, message='')

        # 1. 获取SessionKey
        ok, session_key = self.get_session_key()
        if not ok:
            login_record.message = session_key
            return login_record
        login_record.skey = session_key

        # 2. 获取Index页面和__RequestVerificationToken
        params = {'pSKey': session_key}
        rsp = RequestClient.get_instance().get('https://login.beanfun.com/Login/Index', params=params)
        if rsp.status_code != 200:
            login_record.message = f"获取Index失败，状态码：{rsp.status_code}"
            return login_record
        token_match = re.search(r'<input name="__RequestVerificationToken".*?value="([^"]+?)"', rsp.text)
        if not token_match:
            login_record.message = '获取__RequestVerificationToken失败'
            return login_record
        form_token = token_match.group(1)
        login_record.requestVerificationToken = form_token

        headers = {
            'content-type': 'application/json; charset=utf-8',
            'referer': f'https://login.beanfun.com/Login/Index?pSKey={session_key}',
            'RequestVerificationToken': form_token,
        }

        # 3. CheckAccountType（带check_token）
        check_url = 'https://login.beanfun.com/Login/CheckAccountType'
        params = {'Account': act}
        if check_token:
            params['Captcha'] = check_token
        rsp = RequestClient.get_instance().post(check_url, json=params, headers=headers)
        if rsp.status_code != 200:
            login_record.message = f"CheckAccountType请求失败，状态码：{rsp.status_code}"
            return login_record
        check_entry = TwResponseJson.from_response(rsp)

        # 处理需要reCAPTCHA的情况
        if check_entry.ResultCode != 1:
            if check_entry.ResultData.get('IsRecaptcha', False) and not check_token:
                login_record.isRecaptcha = True
                return login_record
            login_record.message = check_entry.ResultMessage or 'CheckAccountType失败'
            return login_record

        # 检查GamaPass（仍然保留）
        if check_entry.ResultData.get('IsGamaPass'):
            login_record.message = '请使用GamaPass进行登入，登陆器使用【GamaPass】或扫码登录！'
            return login_record

        # 4. AccountLogin（带login_token或服务器回传的captcha）
        login_url = 'https://login.beanfun.com/Login/AccountLogin'
        login_json = {
            'Account': act,
            'Pasw': pwd,
            'IsMobile': False,
        }
        captcha = login_token or check_entry.ResultData.get('Captcha', '')
        if captcha:
            login_json['Captcha'] = captcha

        rsp = RequestClient.get_instance().post(login_url, headers=headers, json=login_json)
        if rsp.status_code != 200:
            login_record.message = f"AccountLogin请求失败，状态码：{rsp.status_code}"
            return login_record
        login_entry = TwResponseJson.from_response(rsp)

        # 处理返回结果
        if login_entry.ResultCode == 1:
            if login_entry.Result == 1:
                # 需要进阶验证（无URL）
                login_record.status = True
                login_record.adv_status = True
                login_record.location = None
                return login_record
            # ResultCode=1且Result≠1表示登录成功，继续SendLogin
        elif login_entry.ResultCode == 2:
            if login_entry.ResultMessage == "AccountLock":
                login_record.message = '您的帳號已被鎖定，可聯繫客服人員了解原因'
                return login_record
            else:
                # 进阶验证URL
                login_record.status = True
                login_record.adv_status = True
                login_record.location = login_entry.ResultMessage
                return login_record
        else:
            # 其他错误，包括需要reCAPTCHA
            if login_entry.ResultData.get('IsRecaptcha', False) and not login_token:
                login_record.isRecaptcha = True
                return login_record
            login_record.message = login_entry.ResultMessage or 'AccountLogin失败'
            return login_record

        # 5. SendLogin 获取表单
        send_url = 'https://login.beanfun.com/Login/SendLogin'
        headers_send = {'Referer': f'https://login.beanfun.com/Login/Index?pSKey={session_key}'}
        rsp = RequestClient.get_instance().get(send_url, headers=headers_send)
        if rsp.status_code != 200:
            login_record.message = f"SendLogin请求失败，状态码：{rsp.status_code}"
            return login_record

        # 解析表单（和原逻辑相同，但更健壮）
        payload = {}
        input_tags = re.findall(r'<input[^>]+>', rsp.text, re.IGNORECASE)
        for tag in input_tags:
            name_match = re.search(r'name\s*=\s*[\'"]([^\'"]+)[\'"]', tag, re.IGNORECASE)
            val_match = re.search(r'value\s*=\s*[\'"]([^\'"]*)[\'"]', tag, re.IGNORECASE)
            if name_match and val_match and "type=\"submit\"" not in tag.lower():
                payload[name_match.group(1)] = val_match.group(1)

        if not payload:
            login_record.message = 'SendLogin表单解析失败'
            return login_record

        # 6. POST return.aspx 提取bfWebToken
        return_headers = {'Referer': 'https://login.beanfun.com/'}
        rsp = RequestClient.get_instance().post(
            "https://tw.beanfun.com/beanfun_block/bflogin/return.aspx",
            data=payload, headers=return_headers, allow_redirects=False
        )
        set_cookie = rsp.headers.get("Set-Cookie", "")
        bf_token_match = re.search(r"bfWebToken=([^;]+)", set_cookie)
        if not bf_token_match:
            login_record.message = '获取bfWebToken失败'
            return login_record

        login_record.bfWebToken = bf_token_match.group(1)
        login_record.status = True
        login_record.message = '登录成功！'
        return login_record

    def get_account_list(self, bf_web_token: str) -> ActInfoResult:
        actResult = ActInfoResult()
        # 1. 先访问 auth.aspx 获取 cookie 副作用
        auth_url = "https://tw.beanfun.com/beanfun_block/auth.aspx"
        auth_params = {
            'channel': 'game_zone',
            'page_and_query': 'game_start.aspx?service_code_and_region=610074_T9',
            'web_token': bf_web_token,
        }
        RequestClient.get_instance().get(auth_url, params=auth_params)

        # 2. 访问账号列表页面 game_server_account_list.aspx
        now = datetime.datetime.now()
        str_date_time = f"{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}{now.minute}"
        url = "https://tw.beanfun.com/beanfun_block/game_zone/game_server_account_list.aspx"
        params = {
            'sc': '610074',
            'sr': 'T9',
            'dt': str_date_time,
        }
        rsp = RequestClient.get_instance().get(url, params=params)
        text = html.unescape(rsp.text)

        if rsp.status_code != 200:
            return actResult

        # 解析账号数量上限提示（divServiceAccountAmountLimitNotice）
        self.__parse_account_limit_notice(actResult, text)

        data_list = re.findall(r'onclick="([^"]*)"><div id="(\w+)" sn="(\d+)" name="([^"]+)"', text)
        if not data_list:
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

    def __parse_account_limit_notice(self, actResult: ActInfoResult, text: str):
        """
        解析账号数量上限提示（divServiceAccountAmountLimitNotice）。
        参考原版 Beanfun / maplelink 的实现：
        - 提示包含「進階認證」→ 需要进阶认证，cert_status = False
        - 提示包含数字 → 提取为最大可创建账号数量 account_limit
        """
        notice_list = re.findall(
            r'<div\sid="divServiceAccountAmountLimitNotice"\sclass="InnerContent">(.*?)</div>', text)
        if not notice_list:
            return
        notice = notice_list[0]
        if "進階認證" in notice:
            # 没有做进阶认证
            actResult.cert_status = False
            return
        # 提取数字上限（如「此遊戲最多允許新增帳號數:2」→ 2）
        num_match = re.search(r'\d+', notice)
        if num_match:
            actResult.account_limit = int(num_match.group(0))

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

        # 1. 获取 game_start_step2.aspx，解析 m_objData（sn / data）与账号信息
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

        # 提取 m_objData 中的 sn（即 pollingKey）
        data_list = re.findall(r'"sn"\s*:\s*"([^"]+)"', rsp.text)
        polling_key = data_list[0] if data_list else None

        # 提取 m_objData 中的 data（加密启动数据）
        data_list = re.findall(r'"data"\s*:\s*"([^"]+)"', rsp.text)
        m_obj_data = data_list[0] if data_list else None

        # 提取账号创建时间
        if not account.create_time:
            data_list = re.findall(r'ServiceAccountCreateTime:\s"([^"]+)"', rsp.text)
            account.create_time = data_list[0] if data_list else None

        # 2. 记录服务启动
        url = "https://tw.beanfun.com/beanfun_block/generic_handlers/record_service_start.ashx"
        data = {
            'service_code': '610074',
            'service_region': 'T9',
            'service_account_id': account.id,
            'sotp': account.sn,
            'service_account_display_name': account.name,
            'service_account_create_time': account.create_time,
            'd1kwcwrajahoxa55zwgbiars': m_obj_data,
        }
        rsp = RequestClient.get_instance().post(url, data=data)
        if rsp.status_code != 200:
            return None

        # 分支：当配置开启「优先使用 GGM 获取密令」且本地已安装 GGM 时，
        # 使用 GGM 进行解密，跳过后续第 3/4/5 步。
        # 判断方式：通过注册表扫描 GGM 安装路径，存在则视为已安装。
        # GGM 会读取注册表 MapleStory\\Path 指向的拦截器 exe，启动时把动态密码
        # 通过命令行参数传给拦截器，拦截器再通过命名管道回传给本程序。
        if Config.ggm_first():
            dynamic_pwd = SystemCom.launch_game_via_ggm(polling_key, m_obj_data)
            if dynamic_pwd:
                logging.info('已通过 GGM 解密，并获取到动态密码')
                return dynamic_pwd
            logging.warning('GGM 启动或获取动态密码失败')
            return None

        # 3. 解密 m_objData.data，得到 LaunchTicket
        #    明文结构：LaunchTicket=...&&&&ServiceCode=...&&&&ServiceRegion=...&&&&...
        decrypted = De2Utils.decrypt_ggm_param(m_obj_data)
        launch_ticket = ''
        if decrypted:
            ticket_match = re.search(r'LaunchTicket=([^&]+)', decrypted)
            if ticket_match:
                launch_ticket = ticket_match.group(1)

        # 4. 获取动态密码（新接口 get_webstart_otp_v2.ashx，POST JSON）
        url = "https://tw.beanfun.com/beanfun_block/generic_handlers/get_webstart_otp_v2.ashx"
        json_data = {
            'SN': polling_key,
            'LaunchTicket': launch_ticket,
            'CV': GLOBAL_CONFIG.ggm['cv'],
            'Hash': GLOBAL_CONFIG.ggm['dll_hash'],
            'arch': 'x64',
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        rsp = RequestClient.get_instance().post(url, json=json_data, headers=headers)
        if rsp.status_code != 200:
            return None

        # 5. 解密响应 data，得到动态密码明文
        #    响应格式：{"result":1,"data":"<8字符key><密文hex>","message":null}
        try:
            resp_json = json.loads(rsp.text)
        except Exception:
            return None

        # 校验 result 字段，非 1 表示请求被拒绝
        if resp_json.get('result') != 1:
            logging.error(f"TW: v2 OTP 请求被拒绝: result={resp_json.get('result')}, "
                          f"message={resp_json.get('message')}")
            return None

        otp_data = resp_json.get('data')
        if not otp_data:
            return None

        # 前 8 字符是 DES key，剩余是 hex 密文
        if len(otp_data) < 8:
            logging.error("TW: OTP data 长度不足，无法提取 DES key")
            return None

        return De2Utils.decrypt_ggm_strings(otp_data[8:], otp_data[:8])

    def get_web_url_member_center(self, bf_web_token: str) -> str:
        return 'https://tw.beanfun.com/TW/auth.aspx?channel=member&page_and_query=index_new.aspx&web_token=' + bf_web_token

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
