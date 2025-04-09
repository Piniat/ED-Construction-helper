from datetime import datetime
from tzlocal import get_localzone
import os
import traceback


def log_file_error():
    try:
        if not os.path.isdir('logs'):
            os.mkdir("logs")
        local_tz = get_localzone()
        now = datetime.now(local_tz)
        now = now.strftime("%Y-%m-%d_%H-%M-%S")
        log_path = f"logs/{now}_error_log.txt"
        print(f"Unhandled error detected. Details in log file {log_path}")
        with open(log_path, "a") as log_file:
            traceback.print_exc(file=log_file)
        input("Press enter to exit")
        os._exit(0)
    except Exception as e:
        print("Lol. Error logger errored out :P This really shouldn't happen...")
        print(f"Details: {e}")
        traceback.print_exc()
        input("Press enter to exit")
        os._exit(0)