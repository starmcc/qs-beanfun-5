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
        params = {
            'skey': qr_code_result.session_key
        }
        RequestClient.get_instance().get('https://tw.newlogin.beanfun.com/login/qr_form.aspx', params=params)

        rsp = RequestClient.get_instance().get('https://tw.newlogin.beanfun.com/generic_handlers/get_qrcodeData.ashx', params=params)
        # 检查HTTP响应状态码
        if rsp.status_code != 200:
            qr_code_result.msg = '获取二维码失败,错误代码[0]'
            return qr_code_result
        try:
            # 解析JSON响应
            entry = rsp.json()
        except ValueError as e:
            qr_code_result.msg = f'JSON解析失败：{str(e)}'
            return qr_code_result
        # 检查响应数据结构完整性
        if not isinstance(entry, dict):
            qr_code_result.msg = '获取二维码失败,错误代码[1]'
            return qr_code_result
        # 获取intResult字段并验证
        int_result = entry.get('intResult')
        if int_result is None:
            qr_code_result.msg = '获取二维码失败,错误代码[2]'
            return qr_code_result
        # 检查业务逻辑状态码
        if int_result != 1:
            qr_code_result.msg = entry.get('strOutstring', '获取二维码失败,错误代码[3]')
            return qr_code_result

        qr_code_result.str_encrypt_data = entry.get("strEncryptData")
        qr_code_result.str_encrypt_bcdd_data = entry.get("strEncryptBCDOData")
        rsp = RequestClient.get_instance().get(
            f'https://tw.newlogin.beanfun.com/qrhandler.ashx?u=https://beanfunstor.blob.core.windows.net/redirect/appCheck.html?url=beanfunapp://Q/gameLogin/gtw/{qr_code_result.str_encrypt_data}')
        if rsp.status_code != 200:
            qr_code_result.msg = '获取二维码图片失败,错误代码[0]'
            return qr_code_result
        qr_code_result.status = True
        qr_code_result.qr_image = rsp.content
        return qr_code_result

    def verify_qr_code_success(self, str_encrypt_data: str) -> int:
        data = {
            'status': str_encrypt_data
        }
        rsp = RequestClient.get_instance().post('https://tw.newlogin.beanfun.com/generic_handlers/CheckLoginStatus.ashx', data=data)
        if rsp.status_code != 200:
            return -1

        content = rsp.json()
        return content.get('Result')

    def login(self, session_key: str) -> (bool, str):
        params = {
            'skey': session_key
        }
        headers = {
            'Referer': f'https://tw.newlogin.beanfun.com/login/qr_form.aspx?skey={session_key}'
        }
        rsp = RequestClient.get_instance().get('https://tw.newlogin.beanfun.com/login/qr_step2.aspx', headers=headers, params=params)

        if rsp.status_code != 200:
            return False, ''
        data_list = re.findall(r'akey=(.*)&authkey=(.*)&', rsp.text)
        data_list = data_list[0] if data_list else None
        aKey = data_list[0] if len(data_list) > 0 else None
        authKey = data_list[1] if len(data_list) > 1 else None

        if not aKey or not authKey:
            return False, ''

        params = {
            'akey': aKey,
            'authkey': authKey,
            'bfapp': '1',
        }
        rsp = RequestClient.get_instance().get('https://tw.newlogin.beanfun.com/login/final_step.aspx', params=params)
        if rsp.status_code != 200:
            return False, ''
        token = rsp.cookies.get("bfWebToken")
        data = {
            'SessionKey': session_key,
            'AuthKey': aKey,
            'ServiceCode': '',
            'ServiceRegion': '',
            'ServiceAccountSN': '0',
        }
        RequestClient.get_instance().post('https://tw.beanfun.com/beanfun_block/bflogin/return.aspx', data=data)
        return True, token
