import os
from modules import state, extract_update
import platform
import time
import ctypes
import sys

def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        os._exit(0)

def extract():
    global platform
    platform = platform.system().lower()
    if platform == 'windows':
        run_as_admin()
        state.user_os = "windows"
    elif platform == 'linux':
        state.user_os = "linux"
    else:
        print("Unsupported platform")
        return
    filename = state.user_os + ".zip"
    extract_update.extractor()
    os.remove(filename)
    print("removed file")
    print("Update Complete. Please restart the app")
    time.sleep(2)
    os._exit(0)

extract()