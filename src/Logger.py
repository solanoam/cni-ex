"""
Written by
Noam Solan - 204484703
Yarin Kimhi - 308337641
repo - https://github.com/solanoam/cni-ex
"""

import datetime
from enum import Enum

class LoggingLevel(Enum):
    """
    enum for logging levels
    """
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    EXCEPTION = 5

class Logger:
    """
    logger for logging messages. can be implemented with any text base class
    """
    def __init__(self, log_level):
        """
        constructor log levels
        :param log_level: level of the current log
        """
        self.log = print
        self.log_level = log_level

    def _log_msg(self, msg, now, prefix):
        """
        logging formatted message
        :param msg: message
        :param now: time
        :param prefix: log level name
        :return:
        """
        self.log(f"[{now}][{prefix}] - {msg}")

    def _log_msg_hierarchy(self, msg, log_level):
        """
        managing heirchy of log messages and weather they should be logged
        :param msg: message
        :param log_level: log level
        :return:
        """
        if self.log_level > LoggingLevel[log_level].value: return
        now = self.now_datetime()
        self._log_msg(msg, now, log_level)

    def now_datetime(self):
        """
        getting current time
        :return: formatted datetime
        """
        return datetime.datetime.now().strftime("%I:%M:%S.%f %p on %B %d, %Y")

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
