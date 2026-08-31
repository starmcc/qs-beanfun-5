import ctypes
import logging
import subprocess
import time
from ctypes import wintypes
from pathlib import Path
from typing import Tuple

import psutil
from PySide6.QtWidgets import QFileDialog

from src.config import Config
from src.config.GlobalConfig import GLOBAL_CONFIG, ActType
from src.plugins import PluginTools
from src.plugins.LocaleRemulator import LocaleRemulator
from src.utils import BaseTools, SchedulerManager, BoxPop

# 加载 user32 DLL
user32 = ctypes.WinDLL("user32", use_last_error=True)

# 定义一些必要的函数原型
user32.FindWindowW.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
user32.FindWindowW.restype = wintypes.HWND

user32.IsZoomed.argtypes = [wintypes.HWND]
user32.IsZoomed.restype = wintypes.BOOL

user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.PostMessageW.restype = wintypes.BOOL

user32.SetForegroundWindow.argtypes = [wintypes.HWND]
user32.SetForegroundWindow.restype = wintypes.BOOL

user32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
user32.ClientToScreen.restype = wintypes.BOOL

user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
user32.GetClientRect.restype = wintypes.BOOL


# 运行经典版游戏的函数
def run_game_classic(window, act: str = None, pwd: str = None):
    try:
        if not act or not pwd:
            GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, 1, '登录凭证已过期，请重新登录后再试')
            return

        service = "2373"
        if GLOBAL_CONFIG.now_login_type == ActType.TW.value:
            service = "2372"

        # 构建 ngm://launch/ 协议 URL
        timestamp = int(time.time() * 1000)
        ngm_url = (
            f"ngm://launch/ -mode:launch -game:'2982@2141' "
            f"-passarg:'{act} {pwd} {service} 944' "
            f"-position:'GameWeb|https://maplestoryclassic.beanfun.com/Main?af_click_id=' "
            f"-architectureplatform:'none' "
            f"-timestamp:{timestamp}"
        )

        ngm_exe = find_ngm_path()
        if not ngm_exe:
            GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, 4, '未找到NGM，请确认已安装Nexon Game Manager')
            return

        subprocess.Popen(
            [ngm_exe, ngm_url],
            shell=False
        )
    except Exception as e:
        import traceback
        err_msg = f"异常：{str(e)}\n堆栈：{traceback.format_exc()}"
        GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, -999, err_msg)


# 运行游戏的函数
def run_game(window, act: str = None, pwd: str = None):
    try:
        # 如果游戏正在运行,弹出询问是否强制结束进程
        if check_game_running():
            GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, 0,
                                               '检测到游戏运行中,是否强制结束后重新启动游戏?')
            return

        # 加载插件
        PluginTools.build_plugin(LocaleRemulator())

        directory_path = Config.game_path()
        if directory_path == '':
            GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, 1, '请设置游戏目录')
            return

        runParam = './MapleStory.exe'
        pass_input = Config.pass_input()
        if pass_input:
            if act and pwd:
                runParam = f'{runParam} tw.login.maplestory.beanfun.com 8484 BeanFun {act} {pwd}'
            else:
                GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, -1, '免输入模式错误：数据不足!')
                return

        runParam = LocaleRemulator().build_LRProc_cmd() + runParam
        subprocess.Popen(runParam, cwd=directory_path)
        RUN_TIME = time.time()

        # ============================= 内部方法 =============================
        def __closeMapleStoryStartWindow(taskId):
            # 获取窗口句柄
            hwnd = user32.FindWindowW('StartUpDlgClass', 'MapleStory')
            try:
                if hwnd:
                    user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE = 0x0010
            except Exception as e:
                GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, -999, str(e))
            finally:
                if hwnd or time.time() - RUN_TIME >= 30:
                    # 如果获取到了，且超过时间则结束任务
                    SchedulerManager.stop_task(taskId)

        def __stopAutoPatcher(taskId):

            try:
                processes = psutil.process_iter()
                for process in processes:
                    if process.name() != 'Patcher.exe':
                        continue
                    command = f"taskkill /pid {process.pid} /f"
                    result = subprocess.run(command, shell=True, check=True)
                    SchedulerManager.stop_task(taskId)
                    if result.returncode == 0:
                        GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window,
                                                           2,
                                                           '程式自动拦截游戏自动更新程序\n建议使用官方补丁进行手动更新\n如需要使用游戏内置自动更新功能\n请前往设置取消阻止自动更新配置')
                    else:
                        GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, -999, result.stderr.decode('gbk'))
                    break
            finally:
                if time.time() - RUN_TIME >= 30:
                    SchedulerManager.stop_task(taskId)

        # ============================= 内部方法End =============================

        if Config.close_start_window():
            SchedulerManager.do_task(__closeMapleStoryStartWindow, 200)

        if Config.stop_update():
            SchedulerManager.do_task(__stopAutoPatcher, 200)
    except Exception as e:
        GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, -999, str(e))


def _run_game_result(win, status, msg):
    # -999 = 系统异常
    # -1  = 免输入模式错误
    # 0 = 游戏正在运行,不执行
    # 1  = 设置游戏目录
    # 2 = 自动阻止更新成功
    # 3 = 登录凭证已过期，请重新登录后再试
    # 4 = 未找到NGM，请确认已安装Nexon Game Manager
    if status == 1:
        if not BoxPop.question(win, msg):
            return
        # 打开设置界面，让用户设置游戏目录
        from src.window.ConfigWin import ConfigWin
        GLOBAL_CONFIG.win_config = ConfigWin(win)
        GLOBAL_CONFIG.win_config.exec()
        # 设置完成后重新启动游戏
        win.start_clicked()
    elif status == 0:
        # 游戏正在运行
        if BoxPop.question(win, msg):
            kill_mapleStory()
            win.start_clicked()
    elif status == 2:
        logging.info(msg)
        BoxPop.info(win, msg)
    else:
        logging.error(msg)
        BoxPop.warn(win, msg)


def select_game_path() -> Tuple[str, str]:
    directory = QFileDialog.getExistingDirectory(None, "选择新枫之谷游戏目录", "",
                                                 options=QFileDialog.Option.DontResolveSymlinks)
    errorMsg = ""
    if not directory:
        return directory, errorMsg
    if BaseTools.check_cn_path(directory):
        errorMsg = "目录中存在中文,游戏目录不建议使用中文汉字,可能会发生无法预估的错误!"
    Config.game_path(directory)
    return directory, errorMsg


def check_game_running():
    return getMapleStoryHwnd() != 0


def check_game_isZoomed():
    hwnd = getMapleStoryHwnd()
    if hwnd:
        if user32.IsZoomed(hwnd):
            return True
    return False


def getMapleStoryHwnd():
    hwnd = user32.FindWindowW("MapleStoryClassTW", "MapleStory")
    return hwnd if hwnd else 0


def auto_input_act_pwd(act, pwd) -> Tuple[int, str]:
    if not check_game_running():
        msg = '游戏未启动，无法自动输入!'
        logging.info(msg)
        return 1, msg
    if check_game_isZoomed():
        msg = '窗口最大化，无法自动输入!'
        logging.info(msg)
        return 2, msg
    hwnd = getMapleStoryHwnd()
    BASE_WIDTH = 1366
    BASE_HEIGHT = 768
    BASE_INPUT_X = 555
    BASE_INPUT_Y = 310
    rect = wintypes.RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rect))
    current_width = rect.right - rect.left
    current_height = rect.bottom - rect.top
    target_x = int(BASE_INPUT_X * (current_width / BASE_WIDTH))
    target_y = int(BASE_INPUT_Y * (current_height / BASE_HEIGHT))
    point = wintypes.POINT(target_x, target_y)
    user32.ClientToScreen(hwnd, ctypes.byref(point))
    # 前置窗口
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    # ESC关闭弹窗
    __postKey(hwnd, 0x1B)
    time.sleep(0.1)
    # 双击输入框
    click_pos(point.x, point.y, double=True)
    time.sleep(0.1)
    # END
    __postKey(hwnd, 0x23)
    # 清空50位
    for _ in range(50):
        __postKey(hwnd, 0x08)
    __postChars(hwnd, act)
    time.sleep(0.1)
    __postKey(hwnd, 0x09)
    __postChars(hwnd, pwd)
    time.sleep(0.1)
    __postKey(hwnd, 0x0D)
    return 0, ''


def click_pos(screen_x: int, screen_y: int, double: bool = False):
    import ctypes
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    # 鼠标左键按下
    user32.SetCursorPos(screen_x, screen_y)
    user32.mouse_event(0x0002, 0, 0, 0, 0)
    ctypes.windll.kernel32.Sleep(50)
    # 鼠标左键弹起
    user32.mouse_event(0x0004, 0, 0, 0, 0)
    if double:
        ctypes.windll.kernel32.Sleep(50)
        user32.mouse_event(0x0002, 0, 0, 0, 0)
        ctypes.windll.kernel32.Sleep(50)
        user32.mouse_event(0x0004, 0, 0, 0, 0)


def __postKey(hwnd, w_param):
    user32.PostMessageW(hwnd, 0x0100, w_param, 0)  # WM_KEYDOWN = 0x0100


def __postChars(hwnd, str_text):
    chars = list(str_text)
    for ch in chars:
        v_key = ord(ch)
        user32.PostMessageW(hwnd, 0x0102, v_key, 0)  # WM_CHAR = 0x0102


def kill_mapleStory() -> str:
    # taskkill /f /im MapleStory.exe
    return __kill_process('MapleStory.exe')


def kill_black_xchg() -> str:
    # taskkill /f /im BlackXchg.aes
    return __kill_process('BlackXchg.aes')


def __kill_process(pro_name: str) -> str:
    try:
        result = subprocess.run(f'taskkill /f /im {pro_name}', shell=True, capture_output=True)
        if result.returncode == 0:
            return ''
        else:
            return result.stderr.decode('gbk')
    except Exception as e:
        return f'发生错误:\n{str(e)}'


def find_ngm_path() -> str:
    """查找NGM安装路径，返回NGM64.exe的完整路径，未找到返回None"""
    import winreg
    # 常见注册表路径
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Nexon\NGM'),
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Nexon\NGM'),
    ]
    for hkey, sub_key in reg_paths:
        try:
            with winreg.OpenKey(hkey, sub_key) as key:
                install_path, _ = winreg.QueryValueEx(key, 'InstallPath')
                ngm_exe = Path(install_path) / 'NGM64.exe'
                if ngm_exe.exists():
                    return str(ngm_exe)
        except (FileNotFoundError, OSError):
            continue

    # 注册表未找到，尝试常见默认路径
    default_paths = [
        Path(r'C:\ProgramData\Nexon\NGM\NGM64.exe'),
        Path(r'C:\Program Files (x86)\Nexon\NGM\NGM64.exe'),
        Path(r'C:\Program Files\Nexon\NGM\NGM64.exe'),
    ]
    for ngm_exe in default_paths:
        if ngm_exe.exists():
            return str(ngm_exe)

    return None


# ============================= GGM 启动 =============================

# GGM 新枫之谷路径注册表键（GGM 通过该键读取游戏启动路径）
GGM_MAPLESTORY_REG_PATH = r'SOFTWARE\GAMANIA\MapleStory'
GGM_MAPLESTORY_REG_VALUE = 'Path'

# 命名管道名（与 ggm_interceptor.py 保持一致）
GGM_PIPE_NAME = r'\\.\pipe\qsbeanfun_ggm'


def find_ggm_webstart_path() -> str:
    """扫描注册表查找 GGM（Gamania Games Manager）的安装路径。

    返回 GGMWebStart.exe 的完整路径；未安装则返回 None。
    """
    import winreg
    # GGM 常见注册表位置（含 32/64 位视图）
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\GAMANIA\gamania Games Manager'),
        (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\GAMANIA\gamania Games Manager'),
        (winreg.HKEY_CURRENT_USER, r'SOFTWARE\GAMANIA\gamania Games Manager'),
    ]
    for hkey, sub_key in reg_paths:
        try:
            with winreg.OpenKey(hkey, sub_key) as key:
                # 尝试多种可能的键名
                for value_name in ('InstallPath', 'Path', 'InstallDir', 'InstallLocation'):
                    try:
                        install_path, _ = winreg.QueryValueEx(key, value_name)
                    except (FileNotFoundError, OSError):
                        continue
                    if not install_path:
                        continue
                    ggm_exe = Path(install_path) / 'GGMWebStart.exe'
                    if ggm_exe.exists():
                        return str(ggm_exe)
        except (FileNotFoundError, OSError):
            continue

    # 注册表未找到，尝试常见默认路径
    default_paths = [
        Path(r'C:\Program Files\gamania Games\gamania Games Manager\GGMWebStart.exe'),
        Path(r'C:\Program Files (x86)\gamania Games\gamania Games Manager\GGMWebStart.exe'),
    ]
    for ggm_exe in default_paths:
        if ggm_exe.exists():
            return str(ggm_exe)

    return None


def is_ggm_installed() -> bool:
    """判断本地是否已安装 GGM。"""
    return find_ggm_webstart_path() is not None


def set_ggm_maplestory_path(exe_path: str) -> bool:
    """将 GGM 的新枫之谷路径（注册表 MapleStory\\Path）改为指定 exe 路径。

    GGM 会把该值当作完整可执行文件路径直接启动，因此这里指向主程序
    exe 本身，GGM 启动游戏时会调用主程序并传入含动态密码的启动参数。

    :param exe_path: 要写入的 exe 完整路径
    :return: 是否写入成功
    """
    import winreg
    if not exe_path:
        return False
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, GGM_MAPLESTORY_REG_PATH) as key:
            winreg.SetValueEx(key, GGM_MAPLESTORY_REG_VALUE, 0, winreg.REG_SZ, exe_path)
        return True
    except OSError as e:
        logging.error(f'写入 GGM 新枫之谷路径失败: {str(e)}')
        return False


def _start_ggm_pipe_server(timeout: float = 10.0):
    """启动命名管道服务器，等待拦截器连接并回传动态密码。

    使用 Windows 原生命名管道（ctypes 调用 kernel32），在后台线程中
    创建管道、等待拦截器连接、读取动态密码。

    返回 (result_holder, thread)，其中 result_holder 是单元素列表，
    用于存放接收到的动态密码（或 None）。

    :param timeout: 等待拦截器连接的超时时间（秒）
    """
    import ctypes
    import threading
    from ctypes import wintypes

    kernel32 = ctypes.windll.kernel32

    PIPE_ACCESS_DUPLEX = 0x00000003
    PIPE_TYPE_MESSAGE = 0x00000004
    PIPE_READMODE_MESSAGE = 0x00000002
    PIPE_WAIT = 0x00000000
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    result_holder = [None]

    def _serve():
        # 创建命名管道
        kernel32.CreateNamedPipeW.restype = wintypes.HANDLE
        kernel32.CreateNamedPipeW.argtypes = [
            wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD,
            wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        ]
        h_pipe = kernel32.CreateNamedPipeW(
            GGM_PIPE_NAME,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            1,  # 最多 1 个实例
            4096,  # 输出缓冲区
            4096,  # 输入缓冲区
            0,  # 默认超时
            None,
        )
        if h_pipe == INVALID_HANDLE_VALUE:
            logging.error('创建命名管道失败')
            return

        try:
            # 等待拦截器连接
            kernel32.ConnectNamedPipe.argtypes = [wintypes.HANDLE, wintypes.LPVOID]
            kernel32.ConnectNamedPipe.restype = wintypes.BOOL
            connected = kernel32.ConnectNamedPipe(h_pipe, None)
            if not connected:
                # 可能已连接（ERROR_PIPE_CONNECTED = 535）
                err = ctypes.get_last_error()
                if err != 535:
                    logging.error(f'等待命名管道连接失败: {err}')
                    return

            # 读取数据
            buf = ctypes.create_string_buffer(4096)
            bytes_read = wintypes.DWORD(0)
            kernel32.ReadFile.argtypes = [
                wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
            ]
            kernel32.ReadFile.restype = wintypes.BOOL
            ok = kernel32.ReadFile(h_pipe, buf, 4096, ctypes.byref(bytes_read), None)
            if ok and bytes_read.value > 0:
                text = buf.raw[:bytes_read.value].decode('utf-8', errors='ignore')
                # 格式：账号\n密码
                parts = text.split('\n', 1)
                if len(parts) == 2:
                    result_holder[0] = parts[1].strip()
        finally:
            kernel32.CloseHandle(h_pipe)

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()
    return result_holder, thread


def _extract_ggm_interceptor() -> str:
    """从 qrc 资源中提取 ggm_interceptor.exe 到本地目录，返回其完整路径。

    拦截器 exe 打包在主程序的 qrc 资源中（:/plugins/ggm_interceptor.exe），
    运行时提取到程序目录下的 plugins 目录，供 GGM 调用。

    :return: 拦截器 exe 的完整路径；提取失败返回空字符串
    """
    import os
    from PySide6.QtCore import QFile, QIODevice

    target_dir = BaseTools.build_path('plugins')
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, 'ggm_interceptor.exe')

    # 已存在则直接返回
    if os.path.exists(target_path):
        return target_path

    qrc_path = ':/plugins/ggm_interceptor.exe'
    try:
        qfile = QFile(qrc_path)
        if not qfile.exists() or not qfile.open(QIODevice.OpenModeFlag.ReadOnly):
            logging.error(f'无法读取 qrc 资源: {qrc_path}')
            return ''
        file_data = qfile.readAll()
        qfile.close()
        with open(target_path, 'wb') as f:
            f.write(file_data.data() if hasattr(file_data, 'data') else bytes(file_data))
        return target_path
    except Exception as e:
        logging.error(f'提取 ggm_interceptor.exe 失败: {str(e)}')
        return ''


def launch_game_via_ggm(sn: str, data: str, timeout: float = 10.0):
    """使用 GGM 启动游戏，并通过命名管道获取动态密码。

    通过 GGMWebStart.exe 携带 gamaniagames:// 协议参数启动，
    由 GGM 负责解密。注册表 MapleStory\\Path 已指向拦截器exe,
    GGM 启动游戏时会调用拦截器，拦截器解析动态密码并通过命名管道
    回传，本函数阻塞等待并返回动态密码。

    :param sn: pollingKey（对应启动参数中的 SN）
    :param data: 加密启动数据（对应启动参数中的 Data）
    :param timeout: 等待拦截器回传的超时时间（秒）
    :return: 动态密码字符串；失败或超时返回 None
    """
    ggm_exe = find_ggm_webstart_path()
    if not ggm_exe:
        logging.error('未找到 GGM，无法通过 GGM 解密')
        return None

    # 从 qrc 资源提取拦截器 exe，并将注册表 MapleStory\\Path 指向它
    interceptor_exe = _extract_ggm_interceptor()
    if not interceptor_exe:
        logging.error('提取 GGM 拦截器 exe 失败')
        return None
    set_ggm_maplestory_path(interceptor_exe)

    # 先启动命名管道服务器，等待拦截器回传动态密码
    result_holder, server_thread = _start_ggm_pipe_server(timeout)

    # 构建 GGM 启动参数
    ggm_url = (
        f'gamaniagames://Region=TW;Production&&&&'
        f'SN={sn}&&&&'
        f'Cmd=06006&&&&'
        f'Data={data}'
    )
    try:
        subprocess.Popen([ggm_exe, ggm_url], shell=False)
    except Exception as e:
        logging.error(f'GGM 启动失败: {str(e)}')
        return None

    # 阻塞等待拦截器回传动态密码
    server_thread.join(timeout)
    return result_holder[0]
