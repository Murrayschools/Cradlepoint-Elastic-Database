from utils.advanced_logging import start_logging
import os

def test_logging():
    start_logging()
    assert len(os.listdir("logs")) < 31, "There are files that need to be deleted from logs. There are more than 30 log directories."