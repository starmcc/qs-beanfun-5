import base64
import hashlib
import logging
import os
import subprocess

from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad


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
                timeout=10  # 超时保护，避免命令挂起
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
                timeout=5
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
