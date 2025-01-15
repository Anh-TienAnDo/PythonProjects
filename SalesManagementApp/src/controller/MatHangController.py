import logging
from tkinter import Frame
from templates.MatHangTemplate import MatHangTemplate

class MatHangController: # lấy data rồi đưa vào template
    def __init__(self, frame: Frame):
        logging.info("MatHang Controller")
        self.frame = frame
        self.mat_hang_template = MatHangTemplate(frame)

    def get_all(self):
        logging.info("Get all MatHang")

    def get_by_id(self, id):
        logging.info(f"Get MatHang with id: {id}")

    def create(self, mat_hang):
        logging.info(f"Create MatHang with id: {mat_hang.id}")

    def update(self, id, mat_hang):
        logging.info(f"Update MatHang with id: {id}")

    def delete(self, id):
        logging.info(f"Delete MatHang with id: {id}")