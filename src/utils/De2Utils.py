import base64
import hashlib
import logging
import os
import subprocess

from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad

from src.config.GlobalConfig import GLOBAL_CONFIG


def __get_cpu_disk_code():
    def _run_powershell_cmd(cmd: str) -> str:
        try:
            # 调用PowerShell，关闭shell=True避免注入风险，捕获标准输出/错误
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", cmd],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                errors="ignore",
                timeout=10,  # 超时保护，避免命令挂起
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            output_lines = [line.strip() for line in result.stdout.split("\n") if line.strip()]
            return output_lines[0] if output_lines else ""
        except subprocess.TimeoutExpired:
            logging.error("PowerShell命令执行超时")
            return ""
        except Exception as e:
            logging.error(f"PowerShell命令执行失败: {str(e)}")
            return ""

    def get_mac_address():
        """获取物理MAC地址（排除虚拟网卡）"""
        try:
            # Windows原生命令getmac，获取物理网卡MAC
            result = subprocess.run(
                ["getmac", "/NH", "/FO", "CSV"],  # 无表头、CSV格式
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                errors="ignore",
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # 解析输出，过滤虚拟网卡（包含"虚拟"或"VMware"/"Virtual"的跳过）
            mac_list = []
            for line in result.stdout.split("\n"):
                if line.strip() and not any(key in line for key in ["虚拟", "VMware", "Virtual", "Hyper-V"]):
                    mac = line.split(",")[0].strip('"').replace("-", "")
                    mac_list.append(mac)
            # 返回第一个物理网卡的MAC
            return mac_list[0] if mac_list else ""
        except Exception as e:
            logging.warning(f"获取MAC地址失败: {str(e)}")
            return ""

    def _generate_fallback_key() -> str:
        # 生成降级密钥
        hardware_info = [
            get_mac_address(),  # 物理MAC地址
            str(os.cpu_count() or 0),  # CPU核心数
        ]
        # 生成MD5 32位密钥
        fallback_material = "|".join(hardware_info).encode("utf-8")
        return hashlib.md5(fallback_material).hexdigest()

    cpu_id = _run_powershell_cmd("Get-CimInstance Win32_Processor | Select-Object -ExpandProperty ProcessorId")
    disk_sn = _run_powershell_cmd("Get-CimInstance Win32_DiskDrive | Select-Object -ExpandProperty SerialNumber")

    # 校验硬件信息是否有效
    if cpu_id and disk_sn:
        return hashlib.md5((cpu_id + disk_sn).encode("utf-8")).hexdigest()
    else:
        # 硬件信息获取失败，生成降级密钥
        logging.error(f"硬件信息获取失败, 生成降级密钥")
        return _generate_fallback_key()


# 全局AES密钥
GLOBAL_AES_KEY = __get_cpu_disk_code()


def decrypt_des_no_pkcs_hex(text):
    """DES NoPkcs hex 解密算法（保持原逻辑）"""
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
    """AES解密"""
    try:
        key_bytes = GLOBAL_AES_KEY.encode('utf-8')
        ciphertext = base64.b64decode(text.encode('utf-8'))
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        data = unpad(plaintext, AES.block_size)
        return data.decode('utf-8')
    except Exception as e:
        logging.error(f"AES解密失败: {str(e)}")
        return ''


def encrypt_aes(text: str) -> str:
    """AES加密"""
    try:
        key_bytes = GLOBAL_AES_KEY.encode('utf-8')
        text_bytes = text.encode('utf-8')
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded_text = pad(text_bytes, AES.block_size)
        data = cipher.encrypt(padded_text)
        return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        logging.error(f"AES加密失败: {str(e)}")
        return ''


# ================================== GGM DECRYPT ==================================

def decrypt_ggm_param(data: str) -> str:
    """
    GGM WebStart DecryptParam 解密算法

    用于解密 game_start_step2.aspx 返回的 m_objData.data，
    得到形如 "LaunchTicket=...&&&&ServiceCode=...&&&&..." 的明文。

    算法：
    1. 取 data[0] 作为十六进制整数 selector。
    2. 依次尝试替换表（优先 selector % 4、selector % 8，再遍历全部 8 个表）。
    3. 每个字符转成它在替换表中的索引（十六进制），得到 normalized hex。
    4. 从 normalized hex 的 selector + 1 位移取出 8 个字符作为 DES key。
    5. 剩余内容转成 bytes，使用 DES-ECB（Padding=None）解密。
    6. 若解密结果包含 "LaunchTicket=" 则视为成功并返回明文；
       否则尝试下一个表（选错表会得到噪声，无法解出 LaunchTicket）。
    """
    if not data:
        return ""

    try:
        selector = int(data[0], 16)
    except ValueError:
        logging.error("GGM DecryptParam 解密失败: 首字符不是合法的十六进制")
        return ""

    body = data[1:]

    # 优先尝试最可能的表，再遍历全部表（去重）
    order = [selector % 4, selector % len(GLOBAL_CONFIG.ggm['tables'])]
    order.extend(range(len(GLOBAL_CONFIG.ggm['tables'])))
    tried = []
    for index in order:
        if index in tried:
            continue
        tried.append(index)

        table = GLOBAL_CONFIG.ggm['tables'][index]
        try:
            normalized = "".join(format(table.index(c), "x") for c in body)
        except ValueError:
            # 字符不在该表中，跳过
            continue

        key_offset = selector + 1
        if key_offset + 8 > len(normalized):
            continue
        key = normalized[key_offset:key_offset + 8].encode("ascii")

        cipher_hex = normalized[:key_offset] + normalized[key_offset + 8:]

        try:
            des = DES.new(key, DES.MODE_ECB)
            plaintext = des.decrypt(bytes.fromhex(cipher_hex))
            plaintext_str = plaintext.rstrip(b"\x00").decode("utf-8")
        except Exception:
            continue

        # 只有解出 LaunchTicket 字段才说明选对了表
        if "LaunchTicket=" in plaintext_str:
            logging.debug(f"GGM DecryptParam 使用替换表 index={index} 解密成功")
            return plaintext_str

    logging.error("GGM DecryptParam 解密失败: 所有替换表均未解出 LaunchTicket")
    return ""


def decrypt_ggm_strings(hex_ciphertext: str, key_ascii: str) -> str:
    """DES ECB 解密。

    使用 8 字节 ASCII key 对 hex 编码的密文进行 DES ECB 无填充解密，
    去除尾端 null 字节后返回 ASCII 字符串。

    :param hex_ciphertext: hex 编码的密文，例如 ``"4A1B..."``
    :param key_ascii: 8 字节 ASCII key，例如 ``"TESTKEY1"``
    :return: 解密后的 ASCII 字符串；key 长度不为 8、hex 非法或密文长度
             不是 8 的倍数时返回空字符串 ``""``
    """
    if not key_ascii or len(key_ascii) != 8:
        logging.warning("decrypt_ggm_strings: key 长度必须为 8 字节")
        return ""

    try:
        key = key_ascii.encode("ascii")
        ciphertext = bytes.fromhex(hex_ciphertext)
    except (UnicodeEncodeError, ValueError) as e:
        logging.error(f"decrypt_ggm_strings: key 或 hex 密文非法: {str(e)}")
        return ""

    if len(ciphertext) % 8 != 0:
        logging.warning("decrypt_ggm_strings: 密文长度不是 8 的倍数")
        return ""

    try:
        des = DES.new(key, DES.MODE_ECB)
        plaintext = des.decrypt(ciphertext)
    except Exception as e:
        logging.error(f"decrypt_ggm_strings: DES 解密失败: {str(e)}")
        return ""

    # 去除 null 字节并转为 ASCII 字符串
    trimmed = plaintext.split(b"\x00", 1)[0]
    try:
        return trimmed.decode("ascii")
    except UnicodeDecodeError as e:
        logging.error(f"decrypt_ggm_strings: 解密结果非 ASCII: {str(e)}")
        return ""
