from datetime import datetime
import logging
import shutil
import os

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def start_logging():
    date = datetime.now()
    
    log_location = f"logs/{months[date.month-1]}-{date.day}"
    remove_old_logs()

    logger = logging.getLogger(os.environ["LOGGER-NAME"])

    if not os.path.exists(log_location):
        os.mkdir(log_location)

    logging.basicConfig(filename=f"{log_location}/cradlepoint-middleware-{date.hour}-{date.minute}.log", level=logging.INFO)
    return logger

def remove_old_logs():
    # Get all log directories
    all_logs = sorted(os.listdir("logs/"), key=lambda x: os.path.getmtime("logs/"+x))
    # Remove logs until the directory is at 30
    while len(all_logs) > 30:
        shutil.rmtree(f"logs/{all_logs[0]}")
        all_logs.pop(0)

def get_current_logger():
    return logging.getLogger(os.environ["LOGGER-NAME"])
