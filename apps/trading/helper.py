from datetime import time

def is_within_range_time(time: time, start_time: time, end_time: time) -> bool:
    return start_time <= time <= end_time
