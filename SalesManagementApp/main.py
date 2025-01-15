from tkinter import Tk, Frame, Menu
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC, ID
import os
import logging
from contants import *
from src.config.database import Database
from src.config.log import LogConfig
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


def setup_search_index():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    schema = Schema(
        id=ID(stored=True, unique=True),
        ten_hang=TEXT(stored=True),
        ten_ncc=TEXT(stored=True),
        ten_khach_hang=TEXT(stored=True),
        ten_chi_phi=TEXT(stored=True)
    )
    create_in("indexdir", schema)

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
        self.show_frame(self.frame_main)

    # tạo menu chính
    def create_menu(self):
        menu_bar = Menu(self.root)
        nav_menu = Menu(menu_bar, tearoff=0)
        nav_menu.add_command(label=TITLE_MAT_HANG, font=FontType.normal(
        ), command=lambda: self.show_frame(self.frame_mat_hang))
        nav_menu.add_command(label=TITLE_NHAP_HANG, font=FontType.normal(
        ), command=lambda: self.show_frame(self.frame_nhap_hang))
        nav_menu.add_command(label=TITLE_BAN_HANG, font=FontType.normal(
        ), command=lambda: self.show_frame(self.frame_ban_hang))
        nav_menu.add_command(label=TITLE_CHI_PHI, font=FontType.normal(
        ), command=lambda: self.show_frame(self.frame_chi_phi))
        nav_menu.add_command(label=TITLE_KHACH_HANG, font=FontType.normal(
        ), command=lambda: self.show_frame(self.frame_khach_hang))
        nav_menu.add_command(label=TITLE_NCC, font=FontType.normal(
        ), command=lambda: self.show_frame(self.frame_ncc))
        nav_menu.add_command(label=TITLE_BAO_CAO, font=FontType.normal(
        ), command=lambda: self.show_frame(self.frame_bao_cao))
        menu_bar.add_cascade(label="Điều hướng", menu=nav_menu)
        self.root.config(menu=menu_bar)

    def frame_content(self):
        MatHangController(self.frame_main)
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
    # setup_search_index()
    init_template()

#     Label(root, text="Sales Management System", font=("Arial", 20)).pack()
#     Button(root, text="Manage Products", command=self.manage_products).pack(pady=10)
#     Button(root, text="Manage Sales", command=self.manage_sales).pack(pady=10)
#     Button(root, text="Manage Purchases", command=self.manage_purchases).pack(pady=10)
#     Button(root, text="Manage Expenses", command=self.manage_expenses).pack(pady=10)
#     Button(root, text="Reports", command=self.view_reports).pack(pady=10)

# def manage_products(self):
#     self.open_window("Manage Products")

# def manage_sales(self):
#     self.open_window("Manage Sales")

# def manage_purchases(self):
#     self.open_window("Manage Purchases")

# def manage_expenses(self):
#     self.open_window("Manage Expenses")

# def view_reports(self):
#     self.open_window("Reports")

# def open_window(self, title):
#     window = Toplevel(self.root)
#     window.title(title)
#     window.geometry("600x400")
#     Label(window, text=title, font=("Arial", 16)).pack()
#     # Placeholder for each section functionality
#     Label(window, text="Functionality coming soon...", font=("Arial", 12)).pack()
