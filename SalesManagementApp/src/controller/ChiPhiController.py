import logging
from tkinter import Frame
from templates.ChiPhiTemplate import ChiPhiTemplate

class ChiPhiController: # lấy data rồi đưa vào template
    def __init__(self, frame: Frame):
        logging.info("ChiPhi Controller")
        self.frame = frame
        self.chi_phi_template = ChiPhiTemplate(frame)

    def get_all(self):
        logging.info("Get all ChiPhi")

    def get_by_id(self, id):
        logging.info(f"Get ChiPhi with id: {id}")

    def create(self, chi_phi):
        logging.info(f"Create ChiPhi with id: {chi_phi.id}")

    def update(self, id, chi_phi):
        logging.info(f"Update ChiPhi with id: {id}")

    def delete(self, id):
        logging.info(f"Delete ChiPhi with id: {id}")