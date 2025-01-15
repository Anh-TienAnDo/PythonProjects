import logging
from tkinter import Frame
from templates.BaoCaoTemplate import BaoCaoTemplate

class BaoCaoController:
    def __init__(self, frame: Frame):
        logging.info("BaoCao Controller")
        self.frame = frame
        self.bao_cao_template = BaoCaoTemplate(frame)
        
    def get_all(self):
        logging.info("Get all BaoCao")
        
    def get_by_id(self, id):
        logging.info(f"Get BaoCao with id: {id}")
        
    def create(self, bao_cao):
        logging.info(f"Create BaoCao with id: {bao_cao.id}")
        
    def update(self, id, bao_cao):
        logging.info(f"Update BaoCao with id: {id}")
        
    def delete(self, id):
        logging.info(f"Delete BaoCao with id: {id}")

