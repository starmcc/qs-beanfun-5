# -*- coding: utf-8 -*-
"""
GGM 启动拦截器（独立 exe）。

用途：
    将本脚本用 PyInstaller 打包成 exe，并把 GGM 的新枫之谷路径
    （注册表 HKEY_CURRENT_USER\\SOFTWARE\\GAMANIA\\MapleStory\\Path）
    指向该 exe。GGM 启动游戏时会调用本 exe，并把包含动态密码的
    启动命令参数传入。

打包方式（推荐 --noconsole，避免弹出黑窗口）：
    pyinstaller --onefile --noconsole ggm_interceptor.py

工作流程：
    1. 解析 GGM 传入的命令行参数，提取账号与动态密码。
    2. 通过命名管道（Named Pipe）将动态密码发送给主程序。

命令行参数格式（由 GGM 传入）：
    MapleStory.exe tw.login.maplestory.beanfun.com 8484 BeanFun <账号> <动态密码>

命名管道数据格式：
    <账号>\n<动态密码>
"""
import sys

# 命名管道名（与主程序 SystemCom 中保持一致）
PIPE_NAME = r'\\.\pipe\qsbeanfun_ggm'


def hide_console_window():
    """隐藏当前进程的控制台窗口（黑窗口）。

    若以 console 模式打包运行，会弹出一个黑色控制台窗口，
    这里通过 Win32 API 将其隐藏，避免闪烁。
    """
    try:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except Exception:
        pass


def parse_dynamic_password(args):
    """从 GGM 传入的命令行参数中解析账号与动态密码。

    账号与动态密码位于最后两个参数。
    """
    # 过滤掉程序自身路径（.exe / .py）
    params = [a for a in args
              if not a.lower().endswith('.exe')
              and not a.lower().endswith('.py')]

    if len(params) >= 2:
        account = params[-2]
        password = params[-1]
        return account, password
    return None, None


def send_via_pipe(account, password):
    """通过命名管道将动态密码发送给主程序。"""
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.windll.kernel32

    GENERIC_WRITE = 0x40000000
    OPEN_EXISTING = 3

    payload = f'{account}\n{password}'.encode('utf-8')

    try:
        # 打开命名管道
        kernel32.CreateFileW.restype = wintypes.HANDLE
        kernel32.CreateFileW.argtypes = [
            wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
        ]
        h_pipe = kernel32.CreateFileW(
            PIPE_NAME,
            GENERIC_WRITE,
            0,  # 不共享
            None,
            OPEN_EXISTING,
            0,
            None,
        )
        if h_pipe == ctypes.c_void_p(-1).value:
            print(f'打开命名管道失败: {ctypes.get_last_error()}', file=sys.stderr)
            return False

        try:
            # 写入数据
            written = wintypes.DWORD(0)
            kernel32.WriteFile.argtypes = [
                wintypes.HANDLE, wintypes.LPCVOID, wintypes.DWORD,
                ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
            ]
            kernel32.WriteFile.restype = wintypes.BOOL
            ok = kernel32.WriteFile(
                h_pipe, payload, len(payload), ctypes.byref(written), None
            )
            return bool(ok)
        finally:
            kernel32.CloseHandle(h_pipe)
    except Exception as e:
        print(f'通过命名管道发送动态密码失败: {e}', file=sys.stderr)
        return False


def main():
    # 隐藏控制台黑窗口
    hide_console_window()

    args = sys.argv[1:]
    account, password = parse_dynamic_password(args)

    if not account or not password:
        print('未能从启动参数中解析出动态密码', file=sys.stderr)
        print(f'原始参数: {args}', file=sys.stderr)
        sys.exit(1)

    if send_via_pipe(account, password):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
