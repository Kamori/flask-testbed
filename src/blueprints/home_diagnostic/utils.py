from time import time
from src.common.safety_helpers import safe_int

# Todo Turn into simple Class
polling_time_stamp = {"recent_timestamp": None,
                      "poll": None}

def handle_polling_cache(timestamp=None):
    global polling_time_stamp
    print(polling_time_stamp)
    if not timestamp:
        now = int(time())
        difference = now - safe_int(polling_time_stamp['recent_timestamp'])
        if difference > 10:
            polling_time_stamp['poll'] = None
    else:
        polling_time_stamp['recent_timestamp'] = timestamp
        polling_time_stamp['poll'] = True

    return None

def online_status(include_timestamp):
    # check the key
    handle_polling_cache()
    key = False
    if polling_time_stamp['poll']:
        key = True

    if include_timestamp:
        return key, polling_time_stamp['recent_timestamp']

    return key


def set_online_status(poll_timestamp):
    handle_polling_cache(poll_timestamp)
    return None