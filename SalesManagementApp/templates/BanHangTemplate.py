import logging
from tkinter import *
from contants import *
from static.css.FontType import FontType

class BanHangTemplate:
    def __init__(self, frame: Frame):
        self.frame = frame
        label_ban_hang = Label(self.frame, text=TITLE_BAN_HANG, font=FontType.h1)
        label_ban_hang.grid(row=0, column=0, pady=20)