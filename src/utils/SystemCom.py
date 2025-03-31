import logging
import subprocess
import time
import ctypes
from ctypes import wintypes
import psutil
import pyautogui

from src.config import Config
from src.config.GlobalConfig import GLOBAL_PATH_PLUGIN_LR_ZIP, GLOBAL_CONFIG
from src.utils import BaseTools, SchedulerManager

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

# 运行游戏的函数
def run_game(self, act: str = None, pwd: str = None, res_fnc=None):
    try:
        # 加载插件
        BaseTools.extract_build_plugin(GLOBAL_PATH_PLUGIN_LR_ZIP)

        directory_path = Config.game_path()
        if directory_path == '':
            GLOBAL_CONFIG.custom_queue.addTask(res_fnc, (1, '请设置游戏目录'))
            return

        runParam = './MapleStory.exe'
        pass_input = Config.pass_input()
        if pass_input:
            if act and pwd:
                runParam = f'{runParam} tw.login.maplestory.beanfun.com 8484 BeanFun {act} {pwd}'
            else:
                GLOBAL_CONFIG.custom_queue.addTask(res_fnc, (2, '免输入模式错误：数据不足!'))
                return

        lr_exe = BaseTools.build_path(r'plugins\LocaleRemulator\LRProc.exe')
        lr_dll = BaseTools.build_path(r'plugins\LocaleRemulator\LRHookx64.dll')
        cmd = f'"{lr_exe}" "{lr_dll}" tms {runParam}'

        subprocess.Popen(cmd, cwd=directory_path)
        RUN_TIME = time.time()

        # ============================= 内部方法 =============================
        def __closeMapleStoryStartWindow(taskId):
            # 获取窗口句柄
            hwnd = user32.FindWindowW('StartUpDlgClass', 'MapleStory')
            try:
                if hwnd:
                    user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE = 0x0010
            except Exception as e:
                GLOBAL_CONFIG.custom_queue.addTask(res_fnc, (-1, str(e)))
            finally:
                if hwnd or time.time() - RUN_TIME >= 5:
                    # 如果获取到了，且超过5秒则结束任务
                    SchedulerManager.stop_task(taskId)

        def __stopAutoPatcher(taskId):
            processes = psutil.process_iter()
            for process in processes:
                if process.name() != 'Patcher.exe':
                    continue
                command = f"taskkill /pid {process.pid} /f"
                result = subprocess.run(command, shell=True, check=True)
                SchedulerManager.stop_task(taskId)
                if result.returncode == 0:
                    GLOBAL_CONFIG.custom_queue.addTask(res_fnc, (3, '已阻止自动更新'))
                else:
                    GLOBAL_CONFIG.custom_queue.addTask(res_fnc, (4, result.stderr.decode('gbk')))
                break
            if time.time() - RUN_TIME >= 10:
                SchedulerManager.stop_task(taskId)

        # ============================= 内部方法End =============================

        if Config.close_start_window():
            SchedulerManager.do_task(__closeMapleStoryStartWindow, 200)

        if Config.stop_update():
            SchedulerManager.do_task(__stopAutoPatcher, 200)
    except Exception as e:
        res_fnc(-1, str(e))


def check_game_running():
    return getMapleStoryHwnd() != 0


def check_game_isZoomed():
    hwnd = getMapleStoryHwnd()
    if hwnd >= 0:
        if user32.IsZoomed(hwnd):
            return True
    return False


def getMapleStoryHwnd():
    return user32.FindWindowW("MapleStoryClassTW", "MapleStory")


def auto_input_act_pwd(act, pwd):
    if not check_game_running() or check_game_isZoomed():
        logging.info("窗口最大化，不使用自动输入")
        return
    # 操作流程：获取窗口焦点 -> 鼠标点输入框 -> 按End -> 按退格 -> 输入 -> 按TAB -> 输入 -> 回车
    hwnd = getMapleStoryHwnd()
    # 前置游戏窗口
    user32.SetForegroundWindow(hwnd)
    pyautogui.sleep(0.3)
    # 关闭错误提示框
    pyautogui.press('esc')
    pyautogui.sleep(0.1)
    point = wintypes.POINT(510, 340)
    user32.ClientToScreen(hwnd, ctypes.byref(point))
    pyautogui.click(point.x, point.y)
    pyautogui.sleep(0.1)
    pyautogui.press('end')
    for _ in range(50):
        __postKey(hwnd, 0x08)  # VK_BACK = 0x08
    __postChars(hwnd, act)
    pyautogui.sleep(0.1)
    __postKey(hwnd, 0x09)  # VK_TAB = 0x09
    __postChars(hwnd, pwd)
    pyautogui.sleep(0.1)
    __postKey(hwnd, 0x0D)  # VK_RETURN = 0x0D


def __postKey(hwnd, w_param):
    user32.PostMessageW(hwnd, 0x0100, w_param, 0)  # WM_KEYDOWN = 0x0100


def __postChars(hwnd, str_text):
    chars = list(str_text)
    for ch in chars:
        v_key = ord(ch)
        user32.PostMessageW(hwnd, 0x0102, v_key, 0)  # WM_CHAR = 0x0102


def kill_black_xchg() -> str:
    # taskkill /f /im BlackXchg.aes
    try:
        result = subprocess.run('taskkill /f /im BlackXchg.aes', shell=True, capture_output=True)
        if result.returncode == 0:
            return ''
        else:
            return result.stderr.decode('gbk')
    except Exception as e:
        return f'{e}'
