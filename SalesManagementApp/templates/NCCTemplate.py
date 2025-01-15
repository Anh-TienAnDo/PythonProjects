# gọi lại controller khi bấm nút
import logging
from tkinter import *
from contants import *
from static.css.FontType import FontType

class NCCTemplate:
    def __init__(self, frame: Frame):
        self.frame = frame
        # Nội dung của frame_mat_hang
        label_ncc = Label(self.frame, text=TITLE_NCC, font=FontType.h1)
        label_ncc.grid(row=0, column=0, pady=20)