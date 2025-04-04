import pytz
from datetime import datetime
from tzlocal import get_localzone

def convert_timestamp(ed_timestamp):
    utc_time = datetime.strptime(ed_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = pytz.utc.localize(utc_time)
    local_tz = get_localzone()
    local_time = utc_time.astimezone(local_tz)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")