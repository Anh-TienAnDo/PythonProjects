import logging
from tkinter import Frame, StringVar, Toplevel, Checkbutton, Listbox, END
from tkinter import ttk
from contants import *
from templates.DataTableTemplate import DataTableTemplate
from static.css.ButtonType import ButtonType
from static.css.EntryType import EntryType
from static.css.FontType import FontType
from static.css.LabelType import LabelType
from src.entity.NhapHangEntity import NhapHang
from src.service.NhapHangService import NhapHangService
from src.utils.TextNormalization import TextNormalization
from functools import partial


class NhapHangAddController:
    def __init__(self, frame: Frame):
        self.frame = frame
        logging.info("NhapHangAdd Controller")
        self.nhap_hang_service = NhapHangService()  # -------
        # self.nhap_hang_vars = {}  # Lưu trữ các StringVar để lấy giá trị sau này
        self.nhap_hang_list = []  # Lưu trữ các đối tượng NhapHang
        self.search_mat_hang_var = StringVar()
        self.search_ncc_var = StringVar()
        self.total_nhap_hang = StringVar()
        self.total_so_luong = StringVar()
        self.total_thanh_tien = StringVar()
        self.coloumn_title = list(NHAP_HANG_COLUMN_NAMES.values())
        self.coloumn_title.insert(0, "STT")
        
        self.init_sub_frame() # ---Tạo các Frame con---
        self.init_table_data() # ---Tạo bảng dữ liệu---
        self.init_components() # ---Tạo các thành phần giao diện---
        # ---- content_frame ----
        self.refresh_nhap_hang_list()
        
    #  Hàm xử lý sự kiện khi nhập văn bản tìm kiếm hàng hóa
    def on_search_mat_hang(self, event):
        pass
    
    #  Hàm xử lý sự kiện khi chọn hàng hóa từ gợi ý
    def on_suggestion_mat_hang_select(self, event):
        pass
    
    #  Hàm xử lý sự kiện khi nhấn nút tìm kiếm hàng hóa
    def on_search_mat_hang_button_click(self):
        pass
    
    #  Hàm xử lý sự kiện khi nhập văn bản tìm kiếm nhà cung cấp
    def on_search_ncc(self, event):
        pass
    
    #  Hàm xử lý sự kiện khi chọn nhà cung cấp từ gợi ý
    def on_suggestion_ncc_select(self, event):
        pass
    
    #  Hàm xử lý sự kiện khi nhấn nút tìm kiếm nhà cung cấp
    def on_search_ncc_button_click(self):
        pass
    
    def save_all(self):
        pass
    
    #  hàm xử lý giao diện khi chọn hàng hóa từ gợi ý
    def refresh_nhap_hang_list(self):
        pass
    
    def view_delete_hang_nhap(self, index):
        pass
    
    def view_cancel(self):
        pass
        
    def init_sub_frame(self):
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title("Thêm mới nhập hàng")
        self.view_new_top_window.geometry("1080x720")
        self.view_new_top_window.rowconfigure(0, weight=1)
        
        self.sub_frame_left = Frame(self.view_new_top_window, bg=BG_COLOR_FRAME_MAIN)
        self.sub_frame_left.grid(row=0, column=0, sticky="nsew")
        self.sub_frame_right = Frame(self.view_new_top_window, bg=BG_COLOR_FRAME_MAIN)
        self.sub_frame_right.grid(row=0, column=1, sticky="nsew")
        
        self.sub_frame_right_top = Frame(self.sub_frame_right, bg=BG_COLOR_FRAME_MAIN)
        self.sub_frame_right_top.grid(row=0, column=0, sticky="nsew")
        self.sub_frame_right_middle = Frame(self.sub_frame_right, bg=BG_COLOR_FRAME_MAIN)
        self.sub_frame_right_middle.grid(row=1, column=0, sticky="nsew")
        self.sub_frame_right_bottom = Frame(self.sub_frame_right, bg=BG_COLOR_FRAME_MAIN)
        self.sub_frame_right_bottom.grid(row=2, column=0, sticky="nsew")
        
        self.view_new_top_window.columnconfigure(0, weight=1)
        self.view_new_top_window.columnconfigure(1, weight=3)
        self.sub_frame_right.rowconfigure(0, weight=1)
        self.sub_frame_right.rowconfigure(1, weight=5)
        self.sub_frame_right.rowconfigure(2, weight=1)
        self.sub_frame_right.columnconfigure(0, weight=1)
        
        self.sub_frame_right_top.rowconfigure(0, weight=1)
        self.sub_frame_right_top.rowconfigure(1, weight=1)
        self.sub_frame_right_top.columnconfigure(0, weight=1)
        self.sub_frame_right_top.columnconfigure(1, weight=1)
        
        self.sub_frame_right_bottom.rowconfigure(0, weight=1)
        self.sub_frame_right_bottom.columnconfigure(0, weight=1)
        self.sub_frame_right_bottom.columnconfigure(1, weight=1)
        
        self.sub_frame_left.rowconfigure(0, weight=1)
        self.sub_frame_left.rowconfigure(1, weight=1)
        self.sub_frame_left.rowconfigure(2, weight=1)
        self.sub_frame_left.rowconfigure(3, weight=1)
        self.sub_frame_left.columnconfigure(0, weight=1)
        self.sub_frame_left.columnconfigure(1, weight=1)
        
        
    def init_components(self):
        # ---- sub_frame_right_top ----
        head_label = LabelType.h1(self.sub_frame_right_top, "Thêm nhập hàng") # Label trong head_frame
        head_label.grid(row=0, column=0, columnspan=2)
        total_nhap_hang_label = LabelType.h4(self.sub_frame_right_top, text="Tổng nhập hàng:", text_color=TEXT_COLOR_BLUE)
        total_nhap_hang_label.grid(row=1, column=0, sticky="nw")
        total_nhap_hang_value = EntryType.normal(self.sub_frame_right_top, text_var=self.total_nhap_hang)
        total_nhap_hang_value.grid(row=1, column=0, sticky="ne")
        
        total_so_luong_label = LabelType.h4(self.sub_frame_right_top, text="Tổng số lượng:", text_color=TEXT_COLOR_BLUE)
        total_so_luong_label.grid(row=1, column=0, sticky="w")
        total_so_luong_value = EntryType.normal(self.sub_frame_right_top, text_var=self.total_so_luong)
        total_so_luong_value.grid(row=1, column=0, sticky='e')
        
        total_thanh_tien_label = LabelType.h4(self.sub_frame_right_top, text="Tổng thành tiền:", text_color=TEXT_COLOR_BLUE)
        total_thanh_tien_label.grid(row=1, column=0, sticky="sw")
        total_thanh_tien_value = EntryType.normal(self.sub_frame_right_top, text_var=self.total_thanh_tien)
        total_thanh_tien_value.grid(row=1, column=0, sticky='se')
        
        
        # ---- sub_frame_right_bottom ----
        button_add = ButtonType.success(self.sub_frame_right_bottom, "Lưu toàn bộ nhập hàng")
        button_add.config(command=partial(self.save_all))
        button_add.grid(row=0, column=0)
        button_cancel = ButtonType.danger(self.sub_frame_right_bottom, "Hủy")
        button_cancel.config(command=self.view_new_top_window.destroy) # ---------------------------------------------------
        button_cancel.grid(row=0, column=1)
        
        # Tạo ô nhập văn bản (Entry) cho tìm kiếm hàng hóa
        search_input_box = EntryType.blue(self.sub_frame_left, text_var=self.search_mat_hang_var)
        search_input_box.grid(row=0, column=0)
        search_input_box.bind("<KeyRelease>", self.on_search_mat_hang) # Liên kết sự kiện nhập văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.sub_frame_left, "Tìm kiếm")
        search_button.config(command=partial(self.on_search_mat_hang_button_click))
        search_button.grid(row=0, column=1)
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_box = Listbox(self.sub_frame_left, font=FontType.normal(), height=5)
        self.suggestion_box.grid(row=1, column=0)
        self.suggestion_box.bind("<<ListboxSelect>>", self.on_suggestion_mat_hang_select)
        
        # Tạo ô nhập văn bản (Entry) cho tìm kiếm ncc
        search_input_box = EntryType.blue(self.sub_frame_left, text_var=self.search_ncc_var)
        search_input_box.grid(row=2, column=0)
        search_input_box.bind("<KeyRelease>", self.on_search_ncc) # Liên kết sự kiện nhập văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.sub_frame_left, "Tìm kiếm")
        search_button.config(command=partial(self.on_search_ncc_button_click))
        search_button.grid(row=2, column=1)
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_box = Listbox(self.sub_frame_left, font=FontType.normal(), height=5)
        self.suggestion_box.grid(row=3, column=0)
        self.suggestion_box.bind("<<ListboxSelect>>", self.on_suggestion_ncc_select)
        
    def init_table_data(self):
        data_table = DataTableTemplate(self.sub_frame_right_middle)
        self.canvas = data_table.get_canvas()
        self.scrollbar_y = data_table.get_scrollbar_y()
        self.scrollbar_x = data_table.get_scrollbar_x()
        self.scrollable_frame = data_table.get_scrollable_frame()
        
    def destroy_table_data(self):
        self.canvas.destroy()
        self.scrollbar_y.destroy()
        self.scrollbar_x.destroy()
        self.scrollable_frame.destroy()
        
