import base64
import hashlib
import logging
import subprocess

from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad


def __get_cpu_disk_code():
    """
    获取CPU+硬盘序列号，通过md5将其变成32位秘钥
    """
    default_key = hashlib.md5('2024KEYQSBEANFUNACTPWDAESENC'.encode('utf-8')).hexdigest()
    try:
        cpu_command = "wmic cpu get processorid"
        cpu_result = subprocess.check_output(cpu_command, shell=True)
        disk_command = "wmic diskdrive get serialnumber"
        disk_result = subprocess.check_output(disk_command, shell=True)
        cpu_info = cpu_result.decode('utf-8').split('\n')[1].strip()
        if len(cpu_info) == 0:
            return default_key
        disk_info = disk_result.decode('utf-8').split('\n')[1].strip()
        if len(disk_info) == 0:
            return default_key
        return hashlib.md5((cpu_info + disk_info).encode('utf-8')).hexdigest()
    except Exception as e:
        logging.error(e)
        return default_key


GLOBAL_AES_KEY = __get_cpu_disk_code()


def decrypt_des_no_pkcs_hex(text):
    """
    DES NoPkcs hex 解密算法
    """
    if not text or text.isspace():
        return ""
    split = text.split(";")
    if not split or len(split) < 2:
        return ""
    deKey = split[1][:8]
    deVal = split[1][8:]
    ciphertext = bytes.fromhex(deVal)
    des = DES.new(deKey.encode(), DES.MODE_ECB)
    plaintext = des.decrypt(ciphertext)
    return plaintext.decode('utf-8').rstrip('\x00')


def decrypt_aes(text: str) -> str:
    """
    AES解密
    """
    try:
        key_bytes = GLOBAL_AES_KEY.encode('utf-8')
        ciphertext = base64.b64decode(text.encode('utf-8'))
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        data = unpad(plaintext, AES.block_size)
        return data.decode('utf-8')
    except Exception as e:
        logging.error(e)
        return ''


def encrypt_aes(text: str) -> str:
    """
    AES加密
    """
    try:
        key_bytes = GLOBAL_AES_KEY.encode('utf-8')
        text_bytes = text.encode('utf-8')
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded_text = pad(text_bytes, AES.block_size)
        data = cipher.encrypt(padded_text)
        return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        logging.error(e)
        return ''
