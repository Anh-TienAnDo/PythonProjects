import logging
from tkinter import Frame
from templates.KhachHangTemplate import KhachHangTemplate

class KhachHangController: # lấy data rồi đưa vào template
    def __init__(self, frame: Frame):
        logging.info("KhachHang Controller")
        self.frame = frame
        self.khach_hang_template = KhachHangTemplate(frame)

    def get_all(self):
        logging.info("Get all KhachHang")

    def get_by_id(self, id):
        logging.info(f"Get KhachHang with id: {id}")

    def create(self, khach_hang):
        logging.info(f"Create KhachHang with id: {khach_hang.id}")

    def update(self, id, khach_hang):
        logging.info(f"Update KhachHang with id: {id}")

    def delete(self, id):
        logging.info(f"Delete KhachHang with id: {id}")