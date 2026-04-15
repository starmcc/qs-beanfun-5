import re

from src.client import QsClient, RequestClient
from src.client.QsQrClient import QsQrClient
from src.models.QrCodeResult import QrCodeResult


class QsQrClientImpl(QsQrClient):
    def get_qr_code_image(self) -> QrCodeResult:
        RequestClient.get_instance().client.cookies.clear()
        qr_code_result = QrCodeResult()
        ok, qr_code_result.session_key = QsClient.get_instance().get_session_key()
        if not ok:
            qr_code_result.msg = qr_code_result.session_key
            return qr_code_result
        params = {'pSKey': qr_code_result.session_key}
        rsp = RequestClient.get_instance().get('https://login.beanfun.com/Login/Index', params=params)
        if rsp.status_code != 200:
            qr_code_result.msg = 'requestVerificationToken获取失败[0]'
            return qr_code_result
        result = re.search(r'<input name="__RequestVerificationToken".*?value="([^"]+?)"', rsp.text)
        # 取出 token
        qr_code_result.requestVerificationToken = result.group(1)
        if not qr_code_result.requestVerificationToken:
            qr_code_result.msg = 'requestVerificationToken获取失败[1]'
            return qr_code_result
        rsp = RequestClient.get_instance().get('https://login.beanfun.com/Login/InitLogin', params=params)
        if rsp.status_code != 200:
            qr_code_result.msg = f"HTTP请求失败，状态码：{rsp.status_code}"
            return qr_code_result
        try:
            # 解析JSON响应
            entry = rsp.json()
        except ValueError as e:
            qr_code_result.msg = f"JSON解析失败: {str(e)}"
            return qr_code_result

            # 检查响应数据结构完整性
        if not isinstance(entry, dict):
            qr_code_result.msg = f'获取二维码接口请求失败(1)!'
            return qr_code_result

        if entry.get('ResultCode') == 0:
            qr_code_result.msg = entry.get('ResultMessage')
            return qr_code_result
        qr_code_result.status = True
        qr_code_result.qr_image = entry.get('ResultData').get('QRImage')
        return qr_code_result

    def verify_qr_code_success(self, result: QrCodeResult) -> int:
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'Referer': f'https://login.beanfun.com/Login/Index?pSKey={result.session_key}',
            'RequestVerificationToken': result.requestVerificationToken,
        }
        rsp = RequestClient.get_instance().post('https://login.beanfun.com/QRLogin/CheckLoginStatus', headers=headers)
        if rsp.status_code != 200:
            return -1
        content = rsp.json()
        return content.get('ResultCode')

    def login(self, result: QrCodeResult) -> (bool, str):
        headers = {
            'content-type': 'application/json; charset=utf-8',
            'Referer': f'https://login.beanfun.com/Login/Index?pSKey={result.session_key}',
            'RequestVerificationToken': result.requestVerificationToken,
        }
        rsp = RequestClient.get_instance().get('https://login.beanfun.com/QRLogin/QRLogin', headers=headers)

        if rsp.status_code != 200:
            return False, '登录失败[0]'

        rsp = RequestClient.get_instance().get('https://login.beanfun.com/Login/SendLogin')
        if rsp.status_code != 200:
            return False, '登录失败[1]'

        payload = {}
        input_tags = re.findall(r'<input[^>]+>', rsp.text, re.IGNORECASE)
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
            return False, '登录失败[2]'
        headers = {
            'Referer': 'https://login.beanfun.com/'
        }
        rsp = RequestClient.get_instance().post("https://tw.beanfun.com/beanfun_block/bflogin/return.aspx",
                                                data=payload, headers=headers, allow_redirects=False)

        set_cookie_header = rsp.headers.get("Set-Cookie", "")
        match = re.search(r"bfWebToken=([^;]+)", set_cookie_header)
        bfWebToken = match.group(1) if match else None
        if bfWebToken is None or bfWebToken == '':
            return False, '登录失败[3]'
        return True, bfWebToken
