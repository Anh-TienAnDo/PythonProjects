# gọi lại controller khi bấm nút
import logging
from tkinter import *
from contants import *
from static.css.FontType import FontType

class ChiPhiTemplate:
    def __init__(self, frame: Frame):
        self.frame = frame
        # Nội dung của frame_mat_hang
        label_chi_phi = Label(self.frame, text=TITLE_CHI_PHI, font=FontType.h1)
        label_chi_phi.grid(row=0, column=0, pady=20)