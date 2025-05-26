from datetime import datetime
from tzlocal import get_localzone

def generate_one_time_timestamp():
    local_tz = get_localzone()
    now = datetime.now(local_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")