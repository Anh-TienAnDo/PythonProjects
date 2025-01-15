# gọi lại controller khi bấm nút
import logging
from tkinter import *
from contants import *
from static.css.FontType import FontType

class KhachHangTemplate:
    def __init__(self, frame: Frame):
        self.frame = frame
        # Nội dung của frame_mat_hang
        label_khach_hang = Label(self.frame, text=TITLE_KHACH_HANG, font=FontType.h1)
        label_khach_hang.grid(row=0, column=0, pady=20)