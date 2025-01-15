import logging
from tkinter import Frame
from templates.NCCTemplate import NCCTemplate

class NCCController:
    def __init__(self, frame: Frame):
        logging.info("NCC Controller")
        self.frame = frame
        self.ncc_template = NCCTemplate(frame)

    def get_all(self):
        logging.info("Get all NCC")

    def get_by_id(self, id):
        logging.info(f"Get NCC with id: {id}")

    def create(self, ncc):
        logging.info(f"Create NCC with id: {ncc.id}")

    def update(self, id, ncc):
        logging.info(f"Update NCC with id: {id}")

    def delete(self, id):
        logging.info(f"Delete NCC with id: {id}")