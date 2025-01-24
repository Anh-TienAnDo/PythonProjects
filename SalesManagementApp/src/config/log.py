import os
import logging


class LogConfig:
    def __init__(self, log_name):
        self.LOGGING_NAME = log_name

    def setup_logging(self):
        # Cấu hình logging
        logging.basicConfig(
            filename="app.log",  # Tên file log
            level=logging.DEBUG,  # Mức độ log
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Định dạng log
            datefmt="%Y-%m-%d %H:%M:%S",  # Định dạng thời gian
        )
        # logging.info("Logging initialized")
