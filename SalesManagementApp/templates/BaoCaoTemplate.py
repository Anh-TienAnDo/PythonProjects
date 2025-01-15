# gọi lại controller khi bấm nút
import logging
from tkinter import *
from contants import *
from static.css.FontType import FontType

class BaoCaoTemplate:
    def __init__(self, frame: Frame):
        self.frame = frame
        label_bao_cao = Label(self.frame, text=TITLE_BAO_CAO, font=FontType.h1)
        label_bao_cao.grid(row=0, column=0, pady=20)