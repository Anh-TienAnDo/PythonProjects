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


class BaoCaoNhapHangController:
    def __init__(self, frame: Frame):
        logging.info("BaoCaoNhapHang Controller")
        self.frame = frame
        self.nhap_hang_service = NhapHangService()
        self.total_nhap_hang = StringVar()
        self.total_so_luong = StringVar()
        self.total_thanh_tien = StringVar()
        self.coloumn_title = COLUMNS_REPORT_NHAP_HANG
        self.coloumn_title.insert(0, "STT")
        self.date = self.nhap_hang_service.get_day_month_year()
        self.search_var_dict = {
            'day': StringVar(value=""),
            'month': StringVar(value=self.date.get('month')),
            'year': StringVar(value=self.date.get('year')),
        }
        self.init_sub_frame()  # ---Tạo các Frame con---
        self.init_table_data()  # ---Tạo bảng dữ liệu---
        self.init_components()  # ---Tạo các thành phần giao diện---
        # ---- content_frame ----
        self.refresh_nhap_hang_list()
        
    def report(self):
        logging.info("report NhapHang")
        try:
            sort = self.sort_var.get()
            day = self.search_var_dict.get('day').get()
            month = self.search_var_dict.get('month').get()
            year = self.search_var_dict.get('year').get()
            report_nhap_hang_list = self.nhap_hang_service.report(sort=sort, day=day, month=month, year=year)
            return report_nhap_hang_list
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return []
          
    # --- Các hàm xử lý sự kiện ---
    # Hàm xử lý khi nhấn nút tìm kiếm
    def on_search_button_click(self):
        self.refresh_nhap_hang_list()
        
    # Làm mới thanh tìm kiếm
    def refresh_entry_search(self):
        self.search_var_dict['day'].set("")
        self.search_var_dict['month'].set(self.date.get('month'))
        self.search_var_dict['year'].set(self.date.get('year'))
        self.refresh_nhap_hang_list()
            
    # Hàm xử lý khi chọn mục trong Combobox Sort
    def on_sort_selected(self, event):
        self.refresh_nhap_hang_list()
        
    # def export_data(self):
    #     self.nhap_hang_service.export_data(self.get_all())
        
    def init_sub_frame(self):
        self.head_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.content_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.view_new_top_window = None
        # Sử dụng grid để đặt các Frame con trong frame_nhap_hang
        self.head_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        # Đặt trọng số cho các hàng và cột của frame_nhap_hang để các Frame con thay đổi kích thước theo frame_nhap_hang
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=3)
        self.frame.grid_columnconfigure(0, weight=1)
        # ---Tạo các widget trong head_frame---
        self.head_frame.grid_rowconfigure(0, weight=1)
        self.head_frame.grid_rowconfigure(1, weight=1)
        self.head_frame.grid_rowconfigure(2, weight=1)
        self.head_frame.grid_columnconfigure(0, weight=1)
        self.head_frame.grid_columnconfigure(1, weight=1)
        self.head_frame.grid_columnconfigure(2, weight=1)
        self.head_frame.grid_columnconfigure(3, weight=1)
        self.head_frame.grid_columnconfigure(4, weight=1)
        self.head_frame.grid_columnconfigure(5, weight=1)
        
        
    # --- Các hàm giao diện  ---
    def refresh_nhap_hang_list(self):
        '''Lấy dữ liệu từ database và cập nhật giao diện'''
        # Thêm nội dung vào content frame với Scrollbar
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
            
        report_nhap_hang_list = self.report()
        # add title for table
        self.show_column_title()
        # Thêm các Label và Button vào scrollable_frame
        row = 1
        total_nhap_hang_temp = 0
        total_so_luong_temp = 0
        total_thanh_tien_temp = 0
        for nhap_hang in report_nhap_hang_list:
            total_nhap_hang_temp += int(nhap_hang[2])
            total_so_luong_temp += int(nhap_hang[3])
            total_thanh_tien_temp += int(nhap_hang[4])
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            coloumn = 1
            for value in nhap_hang:
                value = TextNormalization.format_number(value)
                label = LabelType.normal(self.scrollable_frame, text=value)
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)
                label.grid(row=row, column=coloumn, padx=5, pady=5)
                coloumn += 1
            
            row += 1
            
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        self.total_nhap_hang.set(TextNormalization.format_number(total_nhap_hang_temp))
        self.total_so_luong.set(TextNormalization.format_number(total_so_luong_temp))
        self.total_thanh_tien.set(TextNormalization.format_number(total_thanh_tien_temp) + f" {MONEY_UNIT}")
    
    def show_column_title(self):
        column = 0
        for j in self.coloumn_title:
            label = LabelType.title(self.scrollable_frame, text=j)
            label.grid(row=0, column=column, padx=5)
            column += 1
            
    def init_components(self):
        # ---- head_frame ----
        head_label = LabelType.h1(self.head_frame, TITLE_REPORT_NHAP_HANG) # Label trong head_frame
        head_label.grid(row=0, column=0)
        
        self.init_search_date()
        # Tạo Combobox cho chức năng sắp xếp
        label_sort = LabelType.normal_blue_white(self.head_frame, "Sắp xếp theo:")
        label_sort.grid(row=2, column=0, sticky="n")
        self.sort_var = StringVar()
        sort_combobox = ttk.Combobox(self.head_frame, textvariable=self.sort_var, font=FontType.normal())
        sort_combobox['values'] = self.nhap_hang_service.get_report_nhap_hang_sort_keys()
        sort_combobox.current(0)
        sort_combobox.grid(row=2, column=0)
        # Liên kết sự kiện chọn mục với hàm xử lý
        sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_selected)
        # total
        total_nhap_hang_label = LabelType.h4(self.head_frame, text="Tổng lần nhập:", text_color=TEXT_COLOR_BLUE)
        total_nhap_hang_label.grid(row=2, column=1, sticky="nw")
        total_nhap_hang_value = EntryType.normal(self.head_frame, text_var=self.total_nhap_hang)
        total_nhap_hang_value.grid(row=2, column=1, sticky="ne")
        
        total_so_luong_label = LabelType.h4(self.head_frame, text="Tổng số lượng:", text_color=TEXT_COLOR_BLUE)
        total_so_luong_label.grid(row=2, column=1, sticky="w")
        total_so_luong_value = EntryType.normal(self.head_frame, text_var=self.total_so_luong)
        total_so_luong_value.grid(row=2, column=1, sticky='e')
        
        total_thanh_tien_label = LabelType.h4(self.head_frame, text="Tổng tiền:", text_color=TEXT_COLOR_BLUE)
        total_thanh_tien_label.grid(row=2, column=1, sticky="sw")
        total_thanh_tien_value = EntryType.normal(self.head_frame, text_var=self.total_thanh_tien)
        total_thanh_tien_value.grid(row=2, column=1, sticky='se')
        
    def init_table_data(self):
        data_table = DataTableTemplate(self.content_frame)
        self.canvas = data_table.get_canvas()
        self.scrollbar_y = data_table.get_scrollbar_y()
        self.scrollbar_x = data_table.get_scrollbar_x()
        self.scrollable_frame = data_table.get_scrollable_frame()
        
    def destroy_table_data(self):
        self.canvas.destroy()
        self.scrollbar_y.destroy()
        self.scrollbar_x.destroy()
        self.scrollable_frame.destroy()
        
    def init_search_date(self):
        # Tạo ô bán văn bản (Entry) cho tìm kiếm
        LabelType.h2(self.head_frame, "Tìm theo ngày/tháng/năm:").grid(row=0, column=1, sticky="e", padx=5) #--set ngay thang nam
        LabelType.normal(self.head_frame, "Ngày:").grid(row=1, column=1, sticky="n")
        EntryType.blue_day(self.head_frame, text_var=self.search_var_dict['day'], ).grid(row=1, column=1, sticky="ne")
        LabelType.normal(self.head_frame, "Tháng:").grid(row=1, column=1)
        EntryType.blue_day(self.head_frame, text_var=self.search_var_dict['month'], ).grid(row=1, column=1, pady=5, sticky="e")
        LabelType.normal(self.head_frame, "Năm:").grid(row=1, column=1, sticky="s")
        EntryType.blue_day(self.head_frame, text_var=self.search_var_dict['year'], ).grid(row=1, column=1, pady=5, sticky="se")
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.head_frame, "Tìm kiếm")
        search_button.config(command=partial(self.on_search_button_click))
        search_button.grid(row=0, column=2, sticky="w")
        # Tạo nút làm mới thanh tìm kiếm
        refresh_button = ButtonType.brown(self.head_frame, "Làm mới tìm kiếm\nvà bảng dữ liệu")
        refresh_button.config(command=partial(self.refresh_entry_search))
        refresh_button.grid(row=0, column=3, sticky="w")
        # export and import 
        # button_export = ButtonType.success(self.head_frame, "Xuất Excel")
        # button_export.grid(row=1, column=3, sticky="nw")
        # button_export.config(command=partial(self.export_data))
