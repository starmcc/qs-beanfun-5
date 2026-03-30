from typing import Tuple, Union, Dict, Any


def result_json(rsp, msg) -> Tuple[bool, Union[Dict[str, Any], str]]:
    # 检查HTTP响应状态码
    if rsp.status_code != 200:
        return False, f"HTTP请求失败，状态码：{rsp.status_code}"

    try:
        # 解析JSON响应
        entry = rsp.json()
    except ValueError as e:
        return False, f'JSON解析失败: {str(e)}'

    # 检查响应数据结构完整性
    if not isinstance(entry, dict):
        return False, f'{msg}失败(1)!'

    # 获取intResult字段并验证
    int_result = entry.get('Result')
    if int_result is None:
        return False, f'{msg}失败(2)!'

    # 检查业务逻辑状态码
    if int_result != 0:
        return False, entry.get('ResultMessage', f'{msg}失败!')

    # 错误请求数不等于0则存在业务问题，需要外部解决
    int_result = entry.get('ErrorSeqNum')
    if int_result != 0:
        return False, entry.get('ResultMessage', f'{msg}失败!')

    return True, entry