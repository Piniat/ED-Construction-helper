from datetime import datetime
from tzlocal import get_localzone
import os
import traceback
import glob
import time


def log_file_error():
    try:
        os.makedirs("logs", exist_ok=True)
        count = 0
        oldest_error_log = None
        local_tz = get_localzone()
        now = datetime.now(local_tz)
        now = now.strftime("%Y-%m-%d_%H-%M-%S")
        log_path = os.path.join("logs", f"{now}_error_log.txt")
        logs_folder = ("logs")
        for file in os.listdir(logs_folder):
            if os.path.isfile(os.path.join(logs_folder, file)):
                count+=1
        if count > 90:
            print(f"Warning 50+ log files detected ({count}). Purging...")
            while count > 30:
                logs_list = glob.glob(os.path.join(logs_folder, '*_error_log*.txt'))
                oldest_error_log = min(logs_list, key=os.path.getctime)
                os.remove(oldest_error_log)
                count -= 1
            print("Logs purged. 30 Newest logs files have been kept")
            time.sleep(0.5)
            print(f"Error details in log file {log_path}")
        else:
            print(f"Unhandled error detected. Details in log file {log_path}")
        with open(log_path, "w") as log_file:
            traceback.print_exc(file=log_file)
        input("Press enter to exit")
        os._exit(0)
    except Exception as e:
        print("Lol. Error logger errored out :P This really shouldn't happen...")
        print(f"Details: {e}")
        traceback.print_exc()
        input("Press enter to exit")
        os._exit(0)

def clear_all_logs():
    last_removed = None
    if os.path.exists("logs"):
        logs_folder = ("logs")
        try:
            for file in os.listdir(logs_folder):
                path = os.path.join(logs_folder, file)
                os.remove(path)
                last_removed = file
            if last_removed == None:
                print("No logs to delete")
        except:
            log_file_error()  
    else:
        print("Error. No logs directory found")