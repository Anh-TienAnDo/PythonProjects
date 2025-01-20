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

class NhapHangController:
    def __init__(self, frame: Frame):
        self.frame = frame
        logging.info("NhapHang Controller")
        self.nhap_hang_service = NhapHangService() # -------
        self.nhap_hang_vars = {}  # Lưu trữ các StringVar để lấy giá trị sau này
        self.total_nhap_hang = StringVar()
        self.total_so_luong = StringVar()
        self.total_thanh_tien = StringVar()
        self.coloumn_title = list(NHAP_HANG_COLUMN_NAMES.values())
        self.coloumn_title.insert(0, "STT")
        self.date = self.nhap_hang_service.get_day_month_year()
        self.search_var_dict = {
            'day': StringVar(value=""),
            'month': StringVar(value=self.date.get('month')),
            'year': StringVar(value=self.date.get('year')),
        }
        self.init_sub_frame() # ---Tạo các Frame con---
        self.init_table_data() # ---Tạo bảng dữ liệu---
        self.init_components() # ---Tạo các thành phần giao diện---
        # ---- content_frame ----
        self.refresh_nhap_hang_list()
        
    def get_all(self):
        logging.info("Get all NhapHang")
        try:
            sort = self.sort_var.get()
            day = self.search_var_dict.get('day').get()
            month = self.search_var_dict.get('month').get()
            year = self.search_var_dict.get('year').get()
            nhap_hang_list = self.nhap_hang_service.get_all(sort=sort, day=day, month=month, year=year)
            return nhap_hang_list
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return []
        
    def get_by_id(self, nhap_hang_id):
        logging.info("Get NhapHang with id: %s", nhap_hang_id)
        try:
            nhap_hang = self.nhap_hang_service.get_by_id(nhap_hang_id)
            self.view_edit_item(nhap_hang)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return None
        
    def create(self):
        logging.info("Create NhapHang")
        nhap_hang_data = {key: var.get() for key, var in self.nhap_hang_vars.items()}
        nhap_hang = NhapHang(**nhap_hang_data)
        try: 
            self.nhap_hang_service.create(nhap_hang)
            self.view_new_top_window.destroy()
            self.nhap_hang_vars.clear()
            self.refresh_nhap_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
    def update(self, nhap_hang_id):
        logging.info("Update NhapHang with id: %s", nhap_hang_id)
        nhap_hang_data = {key: var.get() for key, var in self.nhap_hang_vars.items()}
        nhap_hang = NhapHang(**nhap_hang_data)
        try: 
            self.nhap_hang_service.update(nhap_hang_id, nhap_hang)
            self.view_new_top_window.destroy()
            self.nhap_hang_vars.clear()
            self.refresh_nhap_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
    def delete(self, nhap_hang_id):
        logging.info("Delete NhapHang with id: %s", nhap_hang_id)
        try:
            self.nhap_hang_service.delete(nhap_hang_id)
            self.view_new_top_window.destroy()
            self.refresh_nhap_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
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
        
    # --- Các hàm giao diện  ---
    def refresh_nhap_hang_list(self):
        '''Lấy dữ liệu từ database và cập nhật giao diện'''
        # Thêm nội dung vào content frame với Scrollbar
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
            
        nhap_hang_list = self.get_all()
        # add title for table
        self.show_column_title()
        # Thêm các Label và Button vào scrollable_frame
        row = 1
        total_nhap_hang = len(nhap_hang_list)
        total_so_luong = 0
        total_thanh_tien = 0
        for nhap_hang in nhap_hang_list:
            total_thanh_tien += nhap_hang.gia_nhap
            total_so_luong += nhap_hang.so_luong
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            coloumn = 1
            nhap_hang = nhap_hang.to_dict()
            for key in NHAP_HANG_COLUMN_NAMES.keys():
                value = nhap_hang[key]
                if key == "gia_nhap" or key == "thanh_tien" or key == "so_luong":
                    value = TextNormalization.format_number(value)
                label = LabelType.normal(self.scrollable_frame, text=value)
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)

                label.grid(row=row, column=coloumn, padx=5, pady=5)
                coloumn += 1
                
            # Thêm nút "Xem chi tiết/Sửa"
            view_edit_button = ButtonType.primary(self.scrollable_frame, text="Xem / Sửa")
            view_edit_button.config(command=partial(self.get_by_id, nhap_hang_id=nhap_hang.get('id')))
            view_edit_button.grid(row=row, column=coloumn, padx=5, pady=5)
            # Thêm nút "Xóa"
            delete_button = ButtonType.danger(self.scrollable_frame, text="Xóa")
            delete_button.config(command=partial(self.view_delete_item, nhap_hang=nhap_hang))
            delete_button.grid(row=row, column=coloumn+1, padx=5, pady=5)
            
            row += 1
            
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        self.total_nhap_hang.set(TextNormalization.format_number(total_nhap_hang))
        self.total_so_luong.set(TextNormalization.format_number(total_so_luong))
        self.total_thanh_tien.set(TextNormalization.format_number(total_thanh_tien) + f" {MONEY_UNIT}")
        
    def view_edit_item(self, nhap_hang: NhapHang):
        nhap_hang = nhap_hang.to_dict()
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xem chi tiết / Sửa')
        
        row = 1
        for key, value in NHAP_HANG_COLUMN_NAMES.items():
            self.nhap_hang_vars[key] = StringVar(self.view_new_top_window, value=nhap_hang[key])
            if key == 'id' or key == 'ngay_nhap' or key == 'id_mat_hang':
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.view(self.view_new_top_window, text_var=self.nhap_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            elif key == 'gia_nhap' or key == 'thanh_tien' or key == 'so_luong':
                value = TextNormalization.format_number(value)
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.nhap_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.nhap_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        button_save = ButtonType.success(self.view_new_top_window, text="Lưu")
        button_save.config(command=partial(self.update, nhap_hang_id=nhap_hang.get('id')))
        button_save.grid(row=row+1, column=0, padx=5, pady=5)
        
        button_exit = ButtonType.warning(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=row+1, column=1, padx=5, pady=5)
        
    def view_delete_item(self, nhap_hang: dict):
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xóa hàng nhập')
        
        LabelType.h3(self.view_new_top_window, text=nhap_hang['ten_hang']).grid(row=0, column=0, padx=5, pady=5)
        LabelType.normal(self.view_new_top_window, text="Bạn có chắc chắn muốn xóa hàng nhập này?").grid(row=1, column=0, padx=5, pady=5)

        button_delete = ButtonType.danger(self.view_new_top_window, text="Xóa")
        button_delete.config(command=partial(self.delete, nhap_hang_id=nhap_hang.get('id')))
        button_delete.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        
        button_exit = ButtonType.info(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=2, column=0, padx=5, pady=5, sticky="E")
        
    def show_column_title(self):
        for j in self.coloumn_title:
            label = LabelType.title(self.scrollable_frame, text=j)
            label.grid(row=0, column=self.coloumn_title.index(j), padx=5)
        
    
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
    
    def init_components(self):
        # ---- head_frame ----
        head_label = LabelType.h1(self.head_frame, TITLE_NHAP_HANG) # Label trong head_frame
        head_label.grid(row=0, column=0)
        
        self.init_search_date()
        # button add
        button_add = ButtonType.success(self.head_frame, "Thêm nhập hàng")
        # button_add.config(command=partial(self.view_add_item))
        button_add.grid(row=2, column=0)
        # Tạo Combobox cho chức năng sắp xếp
        label_sort = LabelType.normal_blue_white(self.head_frame, "Sắp xếp theo:")
        label_sort.grid(row=2, column=1, sticky="nw")
        self.sort_var = StringVar()
        sort_combobox = ttk.Combobox(self.head_frame, textvariable=self.sort_var, font=FontType.normal())
        sort_combobox['values'] = self.nhap_hang_service.get_nhap_hang_sort_keys()
        sort_combobox.current(0)
        sort_combobox.grid(row=2, column=1, sticky="W")
        # Liên kết sự kiện chọn mục với hàm xử lý
        sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_selected)
        # total
        total_nhap_hang_label = LabelType.h4(self.head_frame, text="Tổng nhập hàng:")
        total_nhap_hang_label.grid(row=2, column=2, sticky="nw")
        total_nhap_hang_value = EntryType.normal(self.head_frame, text_var=self.total_nhap_hang)
        total_nhap_hang_value.grid(row=2, column=2, sticky="ne")
        
        total_so_luong_label = LabelType.h4(self.head_frame, text="Tổng số lượng:")
        total_so_luong_label.grid(row=2, column=2, sticky="w")
        total_so_luong_value = EntryType.normal(self.head_frame, text_var=self.total_so_luong)
        total_so_luong_value.grid(row=2, column=2, sticky='e')
        
        total_thanh_tien_label = LabelType.h4(self.head_frame, text="Tổng thành tiền:")
        total_thanh_tien_label.grid(row=2, column=2, sticky="sw")
        total_thanh_tien_value = EntryType.normal(self.head_frame, text_var=self.total_thanh_tien)
        total_thanh_tien_value.grid(row=2, column=2, sticky='se')
        
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
        # Tạo ô nhập văn bản (Entry) cho tìm kiếm
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
        refresh_button = ButtonType.brown(self.head_frame, "Làm mới thanh tìm kiếm")
        refresh_button.config(command=partial(self.refresh_entry_search))
        refresh_button.grid(row=0, column=2)