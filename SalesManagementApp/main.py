from tkinter import Tk, Frame, Menu
import os
import logging
from contants import *
from src.config.database import Database
from src.config.log import LogConfig
from src.config.search_whoosh import SearchWhooshMatHang, SearchWhooshNCC, SearchWhooshKhachHang
from static.css.FontType import FontType
from src.controller.MatHangController import MatHangController
from src.controller.NhapHangController import NhapHangController
from src.controller.BanHangController import BanHangController
from src.controller.ChiPhiController import ChiPhiController
from src.controller.KhachHangController import KhachHangController
from src.controller.NCCController import NCCController
from src.controller.BaoCaoController import BaoCaoController
from src.controller.BaoCaoBanHangController import BaoCaoBanHangController
from src.controller.BaoCaoNhapHangController import BaoCaoNhapHangController
from functools import partial
import json

# Database setup
def setup_database():
    db = Database(DATABASE_PATH)
    db.init_tables()


def setup_logging():
    log = LogConfig(LOGGING_PATH)
    log.setup_logging()

def setup_search_index():
    search_whoosh_mat_hang = SearchWhooshMatHang()
    search_whoosh_mat_hang.create_document_ix()
    search_whoosh_ncc = SearchWhooshNCC()
    search_whoosh_ncc.create_document_ix()
    search_whoosh_khach_hang = SearchWhooshKhachHang()
    search_whoosh_khach_hang.create_document_ix()

# Tkinter GUI Setup
class SalesManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE_APP)
        self.root.geometry(SCREEN_SIZE)
        # Điều chỉnh DPI scaling
        if SCALING_ACTIVE:
            self.root.tk.call('tk', 'scaling', SCALING_VALUE)

        # Tạo các Frame (container) cho các giao diện khác nhau
        self.frame_main = Frame(root, bg=BG_COLOR_FRAME_MAIN)
        self.frame_mat_hang = Frame(root, bg=BG_COLOR_FRAME_MAT_HANG)
        self.frame_nhap_hang = Frame(root, bg=BG_COLOR_FRAME_NHAP_HANG)
        self.frame_ban_hang = Frame(root, bg=BG_COLOR_FRAME_BAN_HANG)
        self.frame_chi_phi = Frame(root, bg=BG_COLOR_FRAME_CHI_PHI)
        self.frame_khach_hang = Frame(root, bg=BG_COLOR_FRAME_KHACH_HANG)
        self.frame_ncc = Frame(root, bg=BG_COLOR_FRAME_NCC)
        self.frame_bao_cao = Frame(root, bg=BG_COLOR_FRAME_BAO_CAO)
        self.frame_bao_cao_ban_hang = Frame(root, bg=BG_COLOR_FRAME_BAO_CAO)
        self.frame_bao_cao_nhap_hang = Frame(root, bg=BG_COLOR_FRAME_BAO_CAO)

        # Đặt trọng số cho các hàng và cột để các phần tử thay đổi kích thước theo cửa sổ
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Tạo menu Điều hướng
        self.create_menu()

        # Nội dung của các Frame
        self.frame_content()

        # Hiển thị các Frame 
        self.show_frame(self.frame_mat_hang) # Mặc định hiển thị frame_mat_hang

    # tạo menu chính
    def create_menu(self):
        menu_bar = Menu(self.root)
        nav_menu = Menu(menu_bar, tearoff=0, font=FontType.normal())
        nav_menu.add_command(label=TITLE_MAT_HANG, command=partial(self.show_frame, self.frame_mat_hang))
        nav_menu.add_command(label=TITLE_NHAP_HANG, command=partial(self.show_frame, self.frame_nhap_hang))
        nav_menu.add_command(label=TITLE_BAN_HANG, command=partial(self.show_frame, self.frame_ban_hang))
        nav_menu.add_command(label=TITLE_CHI_PHI, command=partial(self.show_frame, self.frame_chi_phi))
        nav_menu.add_command(label=TITLE_KHACH_HANG, command=partial(self.show_frame, self.frame_khach_hang))
        nav_menu.add_command(label=TITLE_NCC, command=partial(self.show_frame, self.frame_ncc))
        menu_bar.add_cascade(label="QUẢN LÝ", menu=nav_menu)
        
        bao_cao_menu = Menu(menu_bar, tearoff=0, font=FontType.normal())
        bao_cao_menu.add_command(label="Báo cáo bán hàng", command=partial(self.show_frame, self.frame_bao_cao_ban_hang))
        bao_cao_menu.add_command(label="Báo cáo nhập hàng", command=partial(self.show_frame, self.frame_bao_cao_nhap_hang))
        bao_cao_menu.add_command(label="Báo cáo lợi nhuận", command=partial(self.show_frame, self.frame_bao_cao))
        menu_bar.add_cascade(label="BÁO CÁO", menu=bao_cao_menu)
        
        self.root.config(menu=menu_bar)

    def frame_content(self):
        # MatHangController(self.frame_main)
        MatHangController(self.frame_mat_hang)
        NhapHangController(self.frame_nhap_hang)
        BanHangController(self.frame_ban_hang)
        ChiPhiController(self.frame_chi_phi)
        KhachHangController(self.frame_khach_hang)
        NCCController(self.frame_ncc)
        BaoCaoController(self.frame_bao_cao)
        BaoCaoBanHangController(self.frame_bao_cao_ban_hang)
        BaoCaoNhapHangController(self.frame_bao_cao_nhap_hang)

    # Sử dụng grid để đặt các Frame trong cửa sổ chính
    def show_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


def init_template():
    root = Tk()
    SalesManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    setup_logging()
    setup_database()
    setup_search_index()
    init_template()
