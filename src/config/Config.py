import json
import logging
import os

from src.utils import DeUtils, BaseTools


def __get_config(key: str, default=None):
    """
    获取配置文件中指定键的值

    Args:
        key (str): 要获取的键
        default : 要获取的键
    """
    config_path = BaseTools.build_path('config.json')
    if not os.path.exists(config_path):
        return default
    with open(config_path, 'r') as file:
        try:
            config = json.load(file).get(key)
            return config if config is not None else default
        except json.JSONDecodeError as e:
            logging.error(e)
            return default


def __save_config(key: str, value):
    """
    保存配置到配置文件

    Args:
        key (str): 要保存的键
        value: 要保存的值
    """
    config_path = BaseTools.build_path('config.json')
    conf = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as file:
                conf = json.load(file)
        except json.JSONDecodeError as e:
            logging.error(e)
            conf = {}
    with open(config_path, 'w') as file:
        conf.setdefault(key)
        conf[key] = value
        json.dump(conf, file, indent=4)


# =============================================================


def pass_input(value: bool = None):
    key = 'pass_input'
    if value is None:
        # 读取
        return __get_config(key, False)
    __save_config(key, value)
    return None


def stop_update(value: bool = None):
    key = 'stop_update'
    if value is None:
        # 读取
        return __get_config(key, True)
    __save_config(key, value)
    return None


def close_start_window(value: bool = None):
    key = 'close_start_window'
    if value is None:
        # 读取
        return __get_config(key, True)
    __save_config(key, value)
    return None


def game_path(value: str = None):
    key = 'game_path'
    if value is None:
        # 读取
        return __get_config(key, '')
    __save_config(key, value)
    return None


def auto_input(value: bool = None):
    key = 'auto_input'
    if value is None:
        # 读取
        return __get_config(key, True)
    __save_config(key, value)
    return None


def accounts(value: list[dict] = None):
    key = 'accounts'
    new_ls: list[dict] = []
    # ==================== 读取需解密
    if not value:
        # 读取
        ls = list(__get_config(key, []))
        for account in ls:
            # 存在就解密
            act = account.get('account')
            account['account'] = act if not act else DeUtils.decrypt_aes(act)
            pwd = account.get('password')
            account['password'] = pwd if not pwd else DeUtils.decrypt_aes(pwd)
            new_ls.append(account)
        return new_ls
    # ==================== 保存需加密
    for account in value:
        act = account.get('account')
        account['account'] = act if not act else DeUtils.encrypt_aes(act)
        pwd = account.get('password')
        account['password'] = pwd if not pwd else DeUtils.encrypt_aes(pwd)
        new_ls.append(account)
    __save_config(key, tuple(new_ls))
    return None


def account_changes(value: dict, insert: bool = False) -> (bool, str):
    lt = accounts()
    if insert:
        for index, entry in enumerate(lt):
            if entry.get('account') == value.get('account'):
                return False, '已存在此账号!'
        lt.insert(0, value)
    else:
        for index, entry in enumerate(lt):
            if entry.get('account') == value.get('account'):
                lt[index] = value
                break
            if index == len(lt) - 1:
                return False, '找不到该账号!'
    accounts(lt)
    return True, '操作成功!'


def account_get(account: str) -> dict:
    if not account:
        return {}
    lt = accounts()
    for entry in lt:
        if entry.get('account') == account:
            return entry
    return {}


def account_del(account: str) -> bool:
    lt = accounts()
    if not lt or not account:
        return False
    status = False
    for index, entry in enumerate(lt):
        if entry.get('account') == account:
            del lt[index]
            status = True
            break
    if status:
        accounts(lt)
    return status


def account_first(account: str = None):
    lt = accounts()
    if not account:
        return lt[0] if lt else {}
    for index, entry in enumerate(lt):
        if entry.get('account') == account:
            lt.insert(0, lt.pop(index))
            break
    accounts(lt)
    return lt[0]


def remember(value: bool = None):
    key = 'remember'
    if value is None:
        # 读取
        return __get_config(key, True)
    __save_config(key, value)
    return None
