import logging
from tkinter import Frame
from templates.NhapHangTemplate import NhapHangTemplate

class NhapHangController:
    def __init__(self, frame: Frame):
        self.frame = frame
        logging.info("NhapHang Controller")
        self.nhap_hang_template = NhapHangTemplate(frame)
        
    def get_all(self):
        logging.info("Get all NhapHang")
        
    def get_by_id(self, id):
        logging.info(f"Get NhapHang with id: {id}")
        
    def create(self, nhap_hang):
        logging.info(f"Create NhapHang with id: {nhap_hang.id}")
        
    def update(self, id, nhap_hang):
        logging.info(f"Update NhapHang with id: {id}")
        
    def delete(self, id):
        logging.info(f"Delete NhapHang with id: {id}")