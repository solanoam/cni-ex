import datetime
from enum import Enum

class LoggingLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    EXCEPTION = 5

class Logger:
    def __init__(self, log_level):
        self.log = print
        self.log_level = log_level

    def _log_msg(self, msg, now, prefix):
        self.log(f"[{now}]{prefix} - {msg}")

    def _log_msg_hierarchy(self, msg, log_level):
        if self.log_level < LoggingLevel[log_level]: return
        now = self.now_datetime()
        self._log_msg(msg, now, log_level)

    def now_datetime(self):
        return datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

    def debug(self, msg):
        self._log_msg_hierarchy(msg, "DEBUG")

    def info(self, msg):
        self._log_msg_hierarchy(msg, "INFO")

    def warning(self, msg):
        self._log_msg_hierarchy(msg, "WARNING")

    def error(self, msg):
        self._log_msg_hierarchy(msg, "ERROR")

    def exception(self, e):
        self._log_msg_hierarchy(f"encountered exception - {e}", "EXCEPTION")
        raise Exception(e)
