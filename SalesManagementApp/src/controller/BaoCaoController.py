import logging
from tkinter import Frame, StringVar
from tkinter import ttk
from contants import *
from templates.DataTableTemplate import DataTableTemplate
from static.css.ButtonType import ButtonType
from static.css.EntryType import EntryType
from static.css.LabelType import LabelType
from src.service.BaoCaoService import BaoCaoService
from src.utils.TextNormalization import TextNormalization
from functools import partial

class BaoCaoController:
    def __init__(self, frame: Frame):
        logging.info("BaoCao Controller")
        self.frame = frame
        self.bao_cao_service = BaoCaoService()
        self.total_chi_phi = StringVar()
        self.total_doanh_thu = StringVar()
        self.total_loi_nhuan = StringVar()
        self.chi_phi_cao_nhat = StringVar()
        self.doanh_thu_cao_nhat = StringVar()
        self.loi_nhuan_cao_nhat = StringVar()
        self.coloumn_title = COLUMNS_REPORT_LOI_NHUAN
        self.coloumn_title.insert(0, "STT")
        self.date = self.bao_cao_service.get_day_month_year()
        self.search_var_dict = {
            'month': StringVar(value=self.date.get('month')),
            'year': StringVar(value=self.date.get('year'))
        }
        self.init_sub_frame()  # ---Tạo các Frame con---
        self.init_table_data()  # ---Tạo bảng dữ liệu---
        self.init_components()  # ---Tạo các thành phần giao diện---
        # ---- content_frame ----
        self.refresh_bao_cao_list()

    def report(self) -> dict:
        logging.info("report BanHang")
        try:
            month = self.search_var_dict.get('month').get()
            year = self.search_var_dict.get('year').get()
            return self.bao_cao_service.report_loi_nhuan(month=month, year=year)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return {}
          
    # --- Các hàm xử lý sự kiện ---
    # Hàm xử lý khi nhấn nút tìm kiếm
    def on_search_button_click(self):
        self.refresh_bao_cao_list()
        
    # Làm mới thanh tìm kiếm
    def refresh_entry_search(self):
        self.search_var_dict['month'].set(self.date.get('month'))
        self.search_var_dict['year'].set(self.date.get('year'))
        self.refresh_bao_cao_list()

    def init_sub_frame(self):
        self.head_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.content_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.view_new_top_window = None
        # Sử dụng grid để đặt các Frame con trong frame_bao_cao
        self.head_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        # Đặt trọng số cho các hàng và cột của frame_bao_cao để các Frame con thay đổi kích thước theo frame_bao_cao
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=3)
        self.frame.grid_columnconfigure(0, weight=1)
        # ---Tạo các widget trong head_frame---
        self.head_frame.grid_rowconfigure(0, weight=1)
        self.head_frame.grid_rowconfigure(1, weight=1)
        self.head_frame.grid_rowconfigure(2, weight=1)
        self.head_frame.grid_rowconfigure(3, weight=1)
        self.head_frame.grid_columnconfigure(0, weight=1)
        self.head_frame.grid_columnconfigure(1, weight=1)
        self.head_frame.grid_columnconfigure(2, weight=1)
        self.head_frame.grid_columnconfigure(3, weight=1)
        self.head_frame.grid_columnconfigure(4, weight=1)
        self.head_frame.grid_columnconfigure(5, weight=1)
        
        
    # --- Các hàm giao diện  ---
    def refresh_bao_cao_list(self):
        '''Lấy dữ liệu từ database và cập nhật giao diện'''
        # Thêm nội dung vào content frame với Scrollbar
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
            
        report_bao_cao_dict = self.report()
        # add title for table
        self.show_column_title()
        # Thêm các Label và Button vào scrollable_frame
        row = 1
        total_chi_phi_temp = 0
        total_doanh_thu_temp = 0
        total_loi_nhuan_temp = 0
        chi_phi_cao_nhat_temp = {'value': 0, 'day': ''}        
        doanh_thu_cao_nhat_temp = {'value': 0, 'day': ''}
        loi_nhuan_cao_nhat_temp = {'value': 0, 'day': ''}
        for key, value in report_bao_cao_dict.items():
            total_chi_phi_day = int(value.get('chi_phi')) + int(value.get('nhap_hang'))
            total_doanh_thu_day = int(value.get('ban_hang'))
            total_loi_nhuan_day = total_doanh_thu_day - total_chi_phi_day
            total_chi_phi_temp += total_chi_phi_day
            total_doanh_thu_temp += total_doanh_thu_day
            total_loi_nhuan_temp += total_loi_nhuan_day
            if total_chi_phi_day > chi_phi_cao_nhat_temp.get('value'):
                chi_phi_cao_nhat_temp['value'] = total_chi_phi_day
                chi_phi_cao_nhat_temp['day'] = str(key)
            if total_doanh_thu_day > doanh_thu_cao_nhat_temp.get('value'):
                doanh_thu_cao_nhat_temp['value'] = total_doanh_thu_day
                doanh_thu_cao_nhat_temp['day'] = str(key)
            if  total_loi_nhuan_day > loi_nhuan_cao_nhat_temp.get('value'):
                loi_nhuan_cao_nhat_temp['value'] = total_loi_nhuan_day
                loi_nhuan_cao_nhat_temp['day'] = str(key)
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            label_day = LabelType.normal(self.scrollable_frame, text=str(key))
            total_chi_phi_day = self.convert_number(total_chi_phi_day)
            total_doanh_thu_day = self.convert_number(total_doanh_thu_day)
            total_loi_nhuan_day = self.convert_number(total_loi_nhuan_day)
            label_chi_phi = LabelType.normal(self.scrollable_frame, text=total_chi_phi_day)
            label_doanh_thu = LabelType.normal(self.scrollable_frame, text=total_doanh_thu_day)
            label_loi_nhuan = LabelType.normal(self.scrollable_frame, text=total_loi_nhuan_day)
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
                label_day.config(bg=BG_COLOR_LIGHT_BLUE)
                label_chi_phi.config(bg=BG_COLOR_LIGHT_BLUE)
                label_doanh_thu.config(bg=BG_COLOR_LIGHT_BLUE)
                label_loi_nhuan.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            label_day.grid(row=row, column=1, padx=5, pady=5)
            label_chi_phi.grid(row=row, column=2, padx=5, pady=5)
            label_doanh_thu.grid(row=row, column=3, padx=5, pady=5)
            label_loi_nhuan.grid(row=row, column=4, padx=5, pady=5)
            
            row += 1
            
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        self.total_chi_phi.set(self.convert_number(total_chi_phi_temp) + f" {MONEY_UNIT}")
        self.total_doanh_thu.set(self.convert_number(total_doanh_thu_temp) + f" {MONEY_UNIT}")
        self.total_loi_nhuan.set(self.convert_number(total_loi_nhuan_temp) + f" {MONEY_UNIT}")
        self.chi_phi_cao_nhat.set(self.convert_number(chi_phi_cao_nhat_temp.get('value')) + f" {MONEY_UNIT}")
        self.doanh_thu_cao_nhat.set(self.convert_number(doanh_thu_cao_nhat_temp.get('value')) + f" {MONEY_UNIT}")
        self.loi_nhuan_cao_nhat.set(self.convert_number(loi_nhuan_cao_nhat_temp.get('value')) + f" {MONEY_UNIT}")
    
    def convert_number(self, number) -> str:
        if number < 0:
            number = abs(number)
            return f"-{TextNormalization.format_number(str(number))}"
        return TextNormalization.format_number(str(number))
    
    def show_column_title(self):
        column = 0
        for j in self.coloumn_title:
            label = LabelType.title(self.scrollable_frame, text=j)
            label.grid(row=0, column=column, padx=5)
            column += 1
            
    def init_components(self):
        # ---- head_frame ----
        head_label = LabelType.h1(self.head_frame, TITLE_BAO_CAO) # Label trong head_frame
        head_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.init_search_date()
        # chi phi, doanh thu, loi nhuan
        chi_phi_cao_nhat_label = LabelType.normal_blue_white(self.head_frame, text="Chi phí cao nhất:")
        chi_phi_cao_nhat_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        chi_phi_cao_nhat_value = EntryType.view(self.head_frame, text_var=self.chi_phi_cao_nhat)
        chi_phi_cao_nhat_value.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        doanh_thu_cao_nhat_label = LabelType.normal_blue_white(self.head_frame, text="Doanh thu cao nhất:")
        doanh_thu_cao_nhat_label.grid(row=2, column=2, sticky="e", padx=5, pady=5)
        doanh_thu_cao_nhat_value = EntryType.view(self.head_frame, text_var=self.doanh_thu_cao_nhat)
        doanh_thu_cao_nhat_value.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        
        loi_nhuan_cao_nhat_label = LabelType.normal_blue_white(self.head_frame, text="Lợi nhuận cao nhất:")
        loi_nhuan_cao_nhat_label.grid(row=2, column=4, sticky="e", padx=5, pady=5)
        loi_nhuan_cao_nhat_value = EntryType.view(self.head_frame, text_var=self.loi_nhuan_cao_nhat)
        loi_nhuan_cao_nhat_value.grid(row=2, column=5, padx=5, pady=5, sticky='w')
        # total
        total_chi_phi_label = LabelType.normal_blue_white(self.head_frame, text="Tổng chi phí:")
        total_chi_phi_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        total_chi_phi_value = EntryType.view(self.head_frame, text_var=self.total_chi_phi)
        total_chi_phi_value.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        
        total_doanh_thu_label = LabelType.normal_blue_white(self.head_frame, text="Tổng doanh thu:")
        total_doanh_thu_label.grid(row=3, column=2, sticky="e", padx=5, pady=5)
        total_doanh_thu_value = EntryType.view(self.head_frame, text_var=self.total_doanh_thu)
        total_doanh_thu_value.grid(row=3, column=3, padx=5, pady=5, sticky='w')
        
        total_loi_nhuan_label = LabelType.normal_blue_white(self.head_frame, text="Tổng lợi nhuận:")
        total_loi_nhuan_label.grid(row=3, column=4, sticky="e", padx=5, pady=5)
        total_loi_nhuan_value = EntryType.view(self.head_frame, text_var=self.total_loi_nhuan)
        total_loi_nhuan_value.grid(row=3, column=5, padx=5, pady=5, sticky='w')
        
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
        LabelType.normal(self.head_frame, "Tháng:").grid(row=0, column=1, sticky="e", padx=5)
        EntryType.blue_day(self.head_frame, text_var=self.search_var_dict['month']).grid(row=0, column=2, sticky='w')
        LabelType.normal(self.head_frame, "Năm:").grid(row=1, column=1, sticky="e", padx=5)
        EntryType.blue_day(self.head_frame, text_var=self.search_var_dict['year']).grid(row=1, column=2, sticky='w')
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.head_frame, "Tìm kiếm")
        search_button.config(command=partial(self.on_search_button_click))
        search_button.grid(row=0, column=2, sticky="e", padx=5)
        # Tạo nút làm mới thanh tìm kiếm
        refresh_button = ButtonType.brown(self.head_frame, "Làm mới tìm kiếm\nvà bảng dữ liệu")
        refresh_button.config(command=partial(self.refresh_entry_search))
        refresh_button.grid(row=0, column=3)
