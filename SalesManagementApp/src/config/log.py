import os
import logging


class LogConfig:
    def __init__(self, log_name):
        self.LOGGING_NAME = log_name

    def setup_logging(self):
        # Cấu hình logging
        logging.basicConfig(
            filename="app.log",  # Tên file log
            filemode="w",  # Chế độ ghi log
            level=logging.DEBUG,  # Mức độ log
            encoding="utf-8",  # Bảng mã
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Định dạng log
            datefmt="%Y-%m-%d %H:%M:%S",  # Định dạng thời gian
        )
        logging.info("Phầm mềm của Developer: 'Lê Hồng Ánh - 2002 - phone: 0397786311'")
        logging.info("Logging initialized")
