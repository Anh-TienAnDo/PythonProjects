import logging
from tkinter import Frame, StringVar, Toplevel, Checkbutton, Listbox, END
from tkinter import ttk
from contants import *
from templates.DataTableTemplate import DataTableTemplate
from static.css.ButtonType import ButtonType
from static.css.EntryType import EntryType
from static.css.FontType import FontType
from static.css.LabelType import LabelType
from src.entity.ChiPhiEntity import ChiPhi
from src.service.ChiPhiService import ChiPhiService
from src.utils.TextNormalization import TextNormalization
from functools import partial

class ChiPhiController: # lấy data rồi đưa vào template
    def __init__(self, frame: Frame):
        logging.info("ChiPhi Controller")
        self.frame = frame
        self.chi_phi_service = ChiPhiService() # -------
        self.chi_phi_vars = {}  # Lưu trữ các StringVar để lấy giá trị sau này
        self.total_chi_phi = StringVar()
        self.total_quantity = StringVar()
        self.coloumn_title = list(CHI_PHI_COLUMN_NAMES.values())
        self.coloumn_title.insert(0, "STT")
        self.date = self.chi_phi_service.get_day_month_year()
        self.search_var_dict = {
            'day': StringVar(value=""),
            'month': StringVar(value=self.date.get('month')),
            'year': StringVar(value=self.date.get('year')),
        }
        self.init_sub_frame() # ---Tạo các Frame con---
        self.init_table_data() # ---Tạo bảng dữ liệu---
        self.init_components() # ---Tạo các thành phần giao diện---
        
        self.refresh_chi_phi_list()

    def get_all(self):
        logging.info("Get all ChiPhi")
        try:
            sort = self.sort_var.get()
            day = self.search_var_dict.get('day').get()
            month = self.search_var_dict.get('month').get()
            year = self.search_var_dict.get('year').get()
            chi_phi_list = self.chi_phi_service.get_all(sort=sort, day=day, month=month, year=year)
            return chi_phi_list
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return []

    def get_by_id(self, chi_phi_id):
        logging.info("Get ChiPhi with id: %s", chi_phi_id)
        try:
            chi_phi = self.chi_phi_service.get_by_id(chi_phi_id)
            self.view_edit_item(chi_phi)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return None

    def create(self):
        logging.info("Create ChiPhi")
        chi_phi_data = {key: var.get() for key, var in self.chi_phi_vars.items()}
        chi_phi = ChiPhi(**chi_phi_data)
        try: 
            self.chi_phi_service.create(chi_phi)
            self.view_new_top_window.destroy()
            self.chi_phi_vars.clear()
            self.refresh_chi_phi_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            
    def create_and_continue(self):
        logging.info("Create and continue ChiPhi")
        chi_phi_data = {key: var.get() for key, var in self.chi_phi_vars.items()}
        chi_phi = ChiPhi(**chi_phi_data)
        try:
            self.chi_phi_service.create(chi_phi)
            self.view_new_top_window.destroy()
            self.chi_phi_vars.clear()
            self.refresh_chi_phi_list()
            self.view_add_item()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)

    def update(self, chi_phi_id):
        logging.info("Update ChiPhi with id: %s", chi_phi_id)
        chi_phi_data = {key: var.get() for key, var in self.chi_phi_vars.items()}
        chi_phi = ChiPhi(**chi_phi_data)
        try: 
            self.chi_phi_service.update(chi_phi_id, chi_phi)
            self.view_new_top_window.destroy()
            self.chi_phi_vars.clear()
            self.refresh_chi_phi_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)

    def delete(self, chi_phi_id):
        logging.info("Delete ChiPhi with id: %s", chi_phi_id)
        try:
            self.chi_phi_service.delete(chi_phi_id)
            self.view_new_top_window.destroy()
            self.refresh_chi_phi_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
    # --- Các hàm xử lý sự kiện ---
    # Hàm xử lý khi nhấn nút tìm kiếm
    def on_search_button_click(self):
        self.refresh_chi_phi_list()
        
    # Làm mới thanh tìm kiếm
    def refresh_entry_search(self):
        self.search_var_dict['day'].set("")
        self.search_var_dict['month'].set(self.date.get('month'))
        self.search_var_dict['year'].set(self.date.get('year'))
        self.refresh_chi_phi_list()
            
    # Hàm xử lý khi chọn mục trong Combobox Sort
    def on_sort_selected(self, event):
        self.refresh_chi_phi_list()
        
    def export_data(self):
        self.chi_phi_service.export_data(self.get_all())
        
    def import_data(self):
        self.chi_phi_service.import_chi_phi()
        self.refresh_chi_phi_list()
        
    # --- Các hàm giao diện  ---
    def refresh_chi_phi_list(self):
        '''Lấy dữ liệu từ database và cập nhật giao diện'''
        # Thêm nội dung vào content frame với Scrollbar
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
            
        chi_phi_list = self.get_all()
        # add title for table
        self.show_column_title()
        # Thêm các Label và Button vào scrollable_frame
        row = 1
        total_chi_phi = 0
        total_quantity = len(chi_phi_list)
        for chi_phi in chi_phi_list:
            total_chi_phi += chi_phi.gia_chi_phi
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            coloumn = 1
            chi_phi = chi_phi.to_dict()
            for key in CHI_PHI_COLUMN_NAMES.keys():
                value = chi_phi[key]
                if key == "gia_chi_phi":
                    value = TextNormalization.format_number(value)
                label = LabelType.normal(self.scrollable_frame, text=value)
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)

                label.grid(row=row, column=coloumn, padx=5, pady=5)
                coloumn += 1
                
            # Thêm nút "Xem chi tiết/Sửa"
            view_edit_button = ButtonType.primary(self.scrollable_frame, text="Xem / Sửa")
            view_edit_button.config(command=partial(self.get_by_id, chi_phi_id=chi_phi.get('id')))
            view_edit_button.grid(row=row, column=coloumn, padx=5, pady=5)
            # Thêm nút "Xóa"
            delete_button = ButtonType.danger(self.scrollable_frame, text="Xóa")
            delete_button.config(command=partial(self.view_delete_item, chi_phi=chi_phi))
            delete_button.grid(row=row, column=coloumn+1, padx=5, pady=5)
            
            row += 1
            
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        self.total_chi_phi.set(TextNormalization.format_number(total_chi_phi) + f" {MONEY_UNIT}")
        self.total_quantity.set(TextNormalization.format_number(total_quantity))
        
    def view_edit_item(self, chi_phi: ChiPhi):
        chi_phi = chi_phi.to_dict()
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xem chi tiết / Sửa')
        
        row = 1
        for key, value in CHI_PHI_COLUMN_NAMES.items():
            self.chi_phi_vars[key] = StringVar(self.view_new_top_window, value=chi_phi[key])
            if key == 'id' or key == 'ngay_tao':
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.view(self.view_new_top_window, text_var=self.chi_phi_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            elif key == 'gia_chi_phi':
                value = TextNormalization.format_number(value)
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.chi_phi_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.chi_phi_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        button_save = ButtonType.success(self.view_new_top_window, text="Lưu")
        button_save.config(command=partial(self.update, chi_phi_id=chi_phi.get('id')))
        button_save.grid(row=row+1, column=0, padx=5, pady=5)
        
        button_exit = ButtonType.warning(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=row+1, column=1, padx=5, pady=5)
    
    def view_add_item(self):
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Thêm chi phí')
        chi_phi = ChiPhi()
        chi_phi = chi_phi.to_dict()
        row = 1
        for key, value in CHI_PHI_COLUMN_NAMES.items():
            self.chi_phi_vars[key] = StringVar(self.view_new_top_window, value=chi_phi[key])
            if key == 'id' or key == 'ngay_tao':
                continue
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.chi_phi_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        button_add = ButtonType.success(self.view_new_top_window, text="Thêm & tiếp")
        button_add.config(command=partial(self.create_and_continue))
        button_add.grid(row=row+1, column=0, padx=5, pady=5)
        
        button_save = ButtonType.primary(self.view_new_top_window, text="Thêm")
        button_save.config(command=partial(self.create))
        button_save.grid(row=row+1, column=1, padx=5, pady=5)
        
        button_exit = ButtonType.warning(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=row+1, column=2, padx=5, pady=5)
        
    def view_delete_item(self, chi_phi: dict):
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xóa chi phí')
        
        LabelType.h3(self.view_new_top_window, text=chi_phi['ten_chi_phi']).grid(row=0, column=0, padx=5, pady=5)
        LabelType.normal(self.view_new_top_window, text="Bạn có chắc chắn muốn xóa chi phí này?").grid(row=1, column=0, padx=5, pady=5)

        button_delete = ButtonType.danger(self.view_new_top_window, text="Xóa")
        button_delete.config(command=partial(self.delete, chi_phi_id=chi_phi.get('id')))
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
        # Sử dụng grid để đặt các Frame con trong frame_chi_phi
        self.head_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        # Đặt trọng số cho các hàng và cột của frame_chi_phi để các Frame con thay đổi kích thước theo frame_chi_phi
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
        head_label = LabelType.h1(self.head_frame, TITLE_CHI_PHI) # Label trong head_frame
        head_label.grid(row=0, column=0)
        
        self.init_search_date()
        # button add
        button_add = ButtonType.success(self.head_frame, "Thêm chi phí")
        button_add.config(command=partial(self.view_add_item))
        button_add.grid(row=2, column=0)
        # Tạo Combobox cho chức năng sắp xếp
        label_sort = LabelType.normal_blue_white(self.head_frame, "Sắp xếp theo:")
        label_sort.grid(row=2, column=1, sticky="nw")
        self.sort_var = StringVar()
        sort_combobox = ttk.Combobox(self.head_frame, textvariable=self.sort_var, font=FontType.normal())
        sort_combobox['values'] = self.chi_phi_service.get_chi_phi_sort_keys()
        sort_combobox.current(0)
        sort_combobox.grid(row=2, column=1, sticky="W")
        # Liên kết sự kiện chọn mục với hàm xử lý
        sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_selected)
        # total chi phi
        total_quantity_label = LabelType.h4(self.head_frame, "Tổng số lượng:", text_color=TEXT_COLOR_BLUE)
        total_quantity_label.grid(row=2, column=2, sticky="nw")
        total_quantity_value = EntryType.view(self.head_frame, text_var=self.total_quantity)
        total_quantity_value.grid(row=2, column=2, sticky="ne")
        
        total_chi_phi = LabelType.h4(self.head_frame, "Tổng chi phí:", text_color=TEXT_COLOR_BLUE)
        total_chi_phi.grid(row=2, column=2, sticky="w")
        total_chi_phi_value = EntryType.view(self.head_frame, text_var=self.total_chi_phi)
        total_chi_phi_value.grid(row=2, column=2, sticky="e")
        
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
        refresh_button = ButtonType.brown(self.head_frame, "Làm mới tìm kiếm\nvà bảng dữ liệu")
        refresh_button.config(command=partial(self.refresh_entry_search))
        refresh_button.grid(row=0, column=3, sticky="w")
        # export and import 
        button_export = ButtonType.success(self.head_frame, "Xuất Excel")
        button_export.grid(row=1, column=3, sticky="nw")
        button_export.config(command=partial(self.export_data))
        button_import = ButtonType.primary(self.head_frame, "Nhập Excel")
        button_import.grid(row=1, column=3, sticky="ne")
        button_import.config(command=partial(self.import_data))