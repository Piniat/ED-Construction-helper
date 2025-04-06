import os
from modules import state, extract_update
import platform
import time

def extract():
    global platform
    platform = platform.system().lower()
    if platform == 'windows':
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