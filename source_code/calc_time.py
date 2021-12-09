import datetime
import logging

def get_delay(desired_time):
    """argument string
    the time for which the update happens

    calculates the time for which the scheduler should delay in order for it execute at the right time

    return int
    the correct delay
    """
    try:
        assert len(desired_time) == 5
        logging.debug("desired_time appropriate length")
    except:
        logging.error("desired_time inappropriate length")
    
    desired_time = desired_time + ':00'
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_seconds = (datetime.datetime.strptime(current_time, "%H:%M:%S") - datetime.datetime(1900, 1, 1)).total_seconds()

    desired_seconds = (datetime.datetime.strptime(desired_time, "%H:%M:%S") - datetime.datetime(1900, 1, 1)).total_seconds()

    if int(desired_time[0:1] + desired_time[3:4]) < int(current_time[0:1] + current_time[3:4]):
        logging.info("desired time is past 24 hours therefor scheduling for same time next day")
        return (int(desired_seconds - current_seconds)) + 86400

    logging.debug("calculating delay from desired time")
    return (int(desired_seconds - current_seconds))