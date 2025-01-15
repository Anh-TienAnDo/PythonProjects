import logging
from tkinter import Frame
from templates.BanHangTemplate import BanHangTemplate

class BanHangController: # lấy data rồi đưa vào template
    def __init__(self, frame: Frame):
        logging.info("BanHang Controller")
        self.frame = frame
        self.ban_hang_template = BanHangTemplate(frame)

    def get_all(self):
        logging.info("Get all BanHang")

    def get_by_id(self, id):
        logging.info(f"Get BanHang with id: {id}")

    def create(self, ban_hang):
        logging.info(f"Create BanHang with id: {ban_hang.id}")

    def update(self, id, ban_hang):
        logging.info(f"Update BanHang with id: {id}")

    def delete(self, id):
        logging.info(f"Delete BanHang with id: {id}")