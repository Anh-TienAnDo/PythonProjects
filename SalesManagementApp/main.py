from tkinter import Tk, Frame, Menu
import os
import logging
from contants import *
from src.config.database import Database
from src.config.log import LogConfig
from src.config.search_whoosh import SearchWhooshMatHang
from static.css.FontType import FontType
from src.controller.MatHangController import MatHangController
from src.controller.NhapHangController import NhapHangController
from src.controller.BanHangController import BanHangController
from src.controller.ChiPhiController import ChiPhiController
from src.controller.KhachHangController import KhachHangController
from src.controller.NCCController import NCCController
from src.controller.BaoCaoController import BaoCaoController


# Database setup
def setup_database():
    db = Database(DATABASE_PATH)
    db.init_tables()


def setup_logging():
    log = LogConfig(LOGGING_PATH)
    log.setup_logging()

# Whoosh Index setup
# id trùng thì sinh id mới

def setup_search_index():
    search_whoosh_mat_hang = SearchWhooshMatHang()
    search_whoosh_mat_hang.create_document_ix()

# Tkinter GUI Setup
class SalesManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE_APP)
        self.root.geometry(SCREEN_SIZE)

        # Tạo các Frame (container) cho các giao diện khác nhau
        self.frame_main = Frame(root, bg=BG_COLOR_FRAME_MAIN)
        self.frame_mat_hang = Frame(root, bg=BG_COLOR_FRAME_MAT_HANG)
        self.frame_nhap_hang = Frame(root, bg=BG_COLOR_FRAME_NHAP_HANG)
        self.frame_ban_hang = Frame(root, bg=BG_COLOR_FRAME_BAN_HANG)
        self.frame_chi_phi = Frame(root, bg=BG_COLOR_FRAME_CHI_PHI)
        self.frame_khach_hang = Frame(root, bg=BG_COLOR_FRAME_KHACH_HANG)
        self.frame_ncc = Frame(root, bg=BG_COLOR_FRAME_NCC)
        self.frame_bao_cao = Frame(root, bg=BG_COLOR_FRAME_BAO_CAO)

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
        nav_menu.add_command(label=TITLE_MAT_HANG, command=lambda: self.show_frame(self.frame_mat_hang))
        nav_menu.add_command(label=TITLE_NHAP_HANG, command=lambda: self.show_frame(self.frame_nhap_hang))
        nav_menu.add_command(label=TITLE_BAN_HANG, command=lambda: self.show_frame(self.frame_ban_hang))
        nav_menu.add_command(label=TITLE_CHI_PHI, command=lambda: self.show_frame(self.frame_chi_phi))
        nav_menu.add_command(label=TITLE_KHACH_HANG, command=lambda: self.show_frame(self.frame_khach_hang))
        nav_menu.add_command(label=TITLE_NCC, command=lambda: self.show_frame(self.frame_ncc))
        menu_bar.add_cascade(label="Chức Năng Quản Lý", menu=nav_menu)
        self.root.config(menu=menu_bar)
        
        bao_cao_menu = Menu(menu_bar, tearoff=0, font=FontType.normal())
        bao_cao_menu.add_command(label="Báo cáo tồn kho")
        bao_cao_menu.add_command(label="Báo cáo doanh thu")
        bao_cao_menu.add_command(label="Báo cáo lợi nhuận")
        bao_cao_menu.add_command(label="Báo cáo chi phí")
        bao_cao_menu.add_command(label="Báo cáo công nợ")
        menu_bar.add_cascade(label="Báo Cáo", menu=bao_cao_menu)

    def frame_content(self):
        # MatHangController(self.frame_main)
        MatHangController(self.frame_mat_hang)
        NhapHangController(self.frame_nhap_hang)
        BanHangController(self.frame_ban_hang)
        ChiPhiController(self.frame_chi_phi)
        KhachHangController(self.frame_khach_hang)
        NCCController(self.frame_ncc)
        BaoCaoController(self.frame_bao_cao)

    # Sử dụng grid để đặt các Frame trong cửa sổ chính
    def show_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


def init_template():
    logging.info('Starting Sales Management System')
    root = Tk()
    SalesManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    setup_logging()
    logging.info('Starting Sales Management System')
    setup_database()
    setup_search_index()
    init_template()
