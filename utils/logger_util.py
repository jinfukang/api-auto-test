import logging
import time
from utils.yaml_util import read_config_yaml, get_root_path

class LoggerUtils:
    def creat_log(self,logger_name='log'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            self.file_log_path = get_root_path() + "/logs/" + read_config_yaml('log', 'log_name') + str(int(time.time())) + ".log"
            self.file_handler = logging.FileHandler(self.file_log_path,encoding="utf-8")
            file_log_level = str(read_config_yaml('log', 'log_level')).lower()
            if file_log_level == "debug":
                self.file_handler.setLevel(logging.DEBUG)
            if file_log_level == "info":
                self.file_handler.setLevel(logging.INFO)
            if file_log_level == "warning":
                self.file_handler.setLevel(logging.WARNING)
            if file_log_level == "error":
                self.file_handler.setLevel(logging.ERROR)
            self.file_handler.setFormatter(logging.Formatter(read_config_yaml('log', 'log_format')))
            self.logger.addHandler(self.file_handler)

            self.console_handler = logging.StreamHandler()

            console_log_level = str(read_config_yaml('log', 'log_level')).lower()
            if console_log_level == "debug":
                self.console_handler.setLevel(logging.DEBUG)
            if console_log_level == "info":
                self.console_handler.setLevel(logging.INFO)
            if console_log_level == "warning":
                self.console_handler.setLevel(logging.WARNING)
            if console_log_level == "error":
                self.console_handler.setLevel(logging.ERROR)

            self.console_handler.setFormatter(logging.Formatter(read_config_yaml('log', 'log_format')))
            self.logger.addHandler(self.console_handler)

        return self.logger

def log(message):
    LoggerUtils().creat_log().info(message)