import subprocess
import time

import psutil
import pyautogui
import win32con
import win32gui

from src.config import Config
from src.config.GlobalConfig import GLOBAL_PATH_PLUGIN_LR_ZIP, GLOBAL_CONFIG
from src.utils import BaseTools, SchedulerManager


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
            hwnd = win32gui.FindWindow('StartUpDlgClass', 'MapleStory')
            try:
                if hwnd:
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
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


def getMapleStoryHwnd():
    return win32gui.FindWindow("MapleStoryClassTW", "MapleStory")


def auto_input_act_pwd(act, pwd):
    # 操作流程：获取窗口焦点 -> 鼠标点输入框 -> 按End -> 按退格 -> 输入 -> 按TAB -> 输入 -> 回车
    hwnd = getMapleStoryHwnd()
    # 前置游戏窗口
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.sleep(0.3)
    # 关闭错误提示框
    pyautogui.press('esc')
    pyautogui.sleep(0.1)
    windowPoint = win32gui.ClientToScreen(hwnd, (510, 340))
    pyautogui.click(windowPoint[0], windowPoint[1])
    pyautogui.sleep(0.1)
    pyautogui.press('end')
    for _ in range(50):
        __postKey(hwnd, win32con.VK_BACK)
    __postChars(hwnd, act)
    pyautogui.sleep(0.1)
    __postKey(hwnd, win32con.VK_TAB)
    # __postKey(hwnd, win32con.VK_END)
    # for _ in range(20):
    #     __postKey(hwnd, win32con.VK_BACK)
    __postChars(hwnd, pwd)
    pyautogui.sleep(0.1)
    __postKey(hwnd, win32con.VK_RETURN)


def __postKey(hwnd, w_param):
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, w_param, 0)


def __postChars(hwnd, str_text):
    chars = list(str_text)
    for ch in chars:
        v_key = ord(ch)
        win32gui.PostMessage(hwnd, win32con.WM_CHAR, v_key, 0)


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
