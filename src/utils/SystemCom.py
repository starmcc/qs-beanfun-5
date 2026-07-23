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
        directory_path = Config.game_classic_path()
        if not directory_path:
            GLOBAL_CONFIG.custom_queue.addTask(_run_game_result, window, 1, '请设置游戏目录')
            return

        game_dir = Path(directory_path)
        exe_path = game_dir / "Maplestory_Classic.exe"
        # 列表参数
        service = "2373"
        if GLOBAL_CONFIG.now_login_type == ActType.TW.value:
            service = "2372"
        cmd_args = [
            str(exe_path),
            str(act),
            str(pwd),
            service,
            "944"
        ]
        subprocess.Popen(
            cmd_args,
            cwd=str(game_dir),
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
    if status == 1:
        if not BoxPop.question(win, msg):
            return
        directory, err = select_game_path()
        if not directory:
            return
        if err:
            BoxPop.warn(win, err)
            return
        # 重新打开
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


def select_game_classic_path() -> Tuple[str, str]:
    directory = QFileDialog.getExistingDirectory(None, "选择新枫之谷经典版游戏目录", "",
                                                 options=QFileDialog.Option.DontResolveSymlinks)
    errorMsg = ""
    if not directory:
        return directory, errorMsg
    if BaseTools.check_cn_path(directory):
        errorMsg = "目录中存在中文,游戏目录不建议使用中文汉字,可能会发生无法预估的错误!"
    Config.game_classic_path(directory)
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
