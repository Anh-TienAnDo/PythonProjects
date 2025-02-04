import logging
from tkinter import Frame, StringVar, Toplevel, Checkbutton, Listbox, END
from tkinter import ttk
from contants import *
from templates.DataTableTemplate import DataTableTemplate
from static.css.ButtonType import ButtonType
from static.css.EntryType import EntryType
from static.css.FontType import FontType
from static.css.LabelType import LabelType
from src.entity.MatHangEntity import MatHang
from src.service.MatHangService import MatHangService
from src.utils.TextNormalization import TextNormalization
from functools import partial


class MatHangController: # lấy data rồi đưa vào template
    def __init__(self, parent: Frame):
        logging.info("MatHang Controller")
        self.parent = parent
        self.frame = Frame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.mat_hang_service = MatHangService()
        self.mat_hang_vars = {}  # Lưu trữ các StringVar để lấy giá trị sau này
        self.search_var = StringVar()
        self.sort_var = StringVar()
        self.suggestions = []
        self.total_item = StringVar()
        self.total_quantity = StringVar()
        self.column_title = list(MAT_HANG_COLUMN_NAMES.values())
        if 'STT' not in self.column_title:
            self.column_title.insert(0, "STT")
        
        self.init_sub_frame() # ---Tạo các Frame con---
        self.init_components() # ---Tạo các thành phần giao diện---
        self.init_table_data() # ---Tạo bảng dữ liệu---
        self.refresh_mat_hang_list()

    # chech search, filter -> refresh data -> get data
    def get_all(self) -> list[MatHang]:
        logging.info("Get all MatHang")
        try:
            sort = self.sort_var.get()
            keyword = self.search_var.get()
            return self.mat_hang_service.get_all(sort=sort, keyword=keyword)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return []

    def get_by_id(self, mat_hang_id: str):
        logging.info("Get MatHang with id: %s", mat_hang_id)
        try:
            mat_hang = self.mat_hang_service.get_by_id(mat_hang_id)
            self.view_edit_item(mat_hang)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return None

    def create(self):
        logging.info("Create MatHang")
        mat_hang_data = {key: var.get() for key, var in self.mat_hang_vars.items()}
        mat_hang = MatHang(**mat_hang_data)
        try: 
            self.mat_hang_service.create(mat_hang)
            self.view_new_top_window.destroy()
            self.mat_hang_vars.clear()
            self.refresh_mat_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            
    def create_and_continue(self):
        logging.info("Create and continue MatHang")
        mat_hang_data = {key: var.get() for key, var in self.mat_hang_vars.items()}
        mat_hang = MatHang(**mat_hang_data)
        try:
            self.mat_hang_service.create(mat_hang)
            self.view_new_top_window.destroy()
            self.mat_hang_vars.clear()
            self.refresh_mat_hang_list()
            self.view_add_item()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)

    def update(self, mat_hang_id):
        logging.info("Update MatHang with id: %s", mat_hang_id)
        mat_hang_data = {key: var.get() for key, var in self.mat_hang_vars.items()}
        mat_hang = MatHang(**mat_hang_data)
        try: 
            self.mat_hang_service.update(mat_hang_id, mat_hang)
            self.view_new_top_window.destroy()
            self.mat_hang_vars.clear()
            self.refresh_mat_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)

    def delete(self, mat_hang_id: str):
        logging.info("Delete MatHang with id: %s", mat_hang_id)
        try:
            self.mat_hang_service.delete(mat_hang_id)
            self.view_new_top_window.destroy()
            self.refresh_mat_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
    # Hàm xử lý sự kiện nhập văn bản
    def on_search(self, event):
        search_text = self.search_var.get()
        if search_text is not None and search_text.strip() != "":
            self.update_suggestions()

    # Hàm xử lý khi nhấn nút tìm kiếm
    def on_search_button_click(self):
        self.refresh_mat_hang_list()
        
    # Cập nhật danh sách gợi ý khi người dùng nhập từ khóa
    def update_suggestions(self, *args):
        keyword = self.search_var.get()
        self.suggestions = self.mat_hang_service.get_suggestions(keyword)
        self.suggestion_box.delete(0, END)
        for suggestion in self.suggestions:
            self.suggestion_box.insert(END, suggestion)
            
    # Xử lý sự kiện khi người dùng chọn một gợi ý
    def on_suggestion_select(self, event):
        selected_index = self.suggestion_box.curselection()
        if selected_index:
            selected_text = self.suggestion_box.get(selected_index)
            self.search_var.set(selected_text)
        
    # Hàm xử lý khi chọn mục trong Combobox Sort
    def on_sort_selected(self, event):
        self.refresh_mat_hang_list()
        
    # Làm mới thanh tìm kiếm
    def refresh_entry_search(self):
        self.search_var.set("")
        self.suggestion_box.delete(0, END)
        self.refresh_mat_hang_list()
        
    def export_data(self):
        self.search_var.set("") # clear search
        self.mat_hang_service.export_data(self.get_all())
        
    def import_data(self):
        self.mat_hang_service.import_mat_hang()
        self.refresh_mat_hang_list()
        
    # --- các hàm giao diện ---
    def refresh_mat_hang_list(self):
        '''Lấy dữ liệu từ database và cập nhật giao diện: list mặt hàng, tổng số mặt hàng, tổng số lượng'''
        # Thêm nội dung vào frame2 với Scrollbar
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
            
        mat_hang_list = self.get_all()
        total_item_temp = len(mat_hang_list)
        total_quantity_temp = 0
        # add title for table
        self.show_column_title()

        # Thêm các Label và Button vào scrollable_frame
        row = 1
        for mat_hang in mat_hang_list:
            total_quantity_temp += mat_hang.so_luong
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            column = 1
            mat_hang = mat_hang.to_dict()
            for key in MAT_HANG_COLUMN_NAMES.keys():
                value = mat_hang[key]
                if key == "is_active":
                    value = "Còn bán" if value else "Ngừng bán"
                if key == "gia_le" or key == "gia_si" or key == "so_luong":
                    value = TextNormalization.format_number(value)
                label = LabelType.normal(self.scrollable_frame, text=value)
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)
                label.grid(row=row, column=column, padx=5, pady=5)
                column += 1
                
            # Thêm nút "Xem chi tiết/Sửa"
            view_edit_button = ButtonType.primary(self.scrollable_frame, text="Xem / Sửa")
            view_edit_button.config(command=partial(self.get_by_id, mat_hang_id=mat_hang['id']))
            view_edit_button.grid(row=row, column=column, padx=5, pady=5)

            # Thêm nút "Xóa"
            delete_button = ButtonType.danger(self.scrollable_frame, text="Xóa")
            delete_button.config(command=partial(self.view_delete_item, mat_hang=mat_hang))
            delete_button.grid(row=row, column=column+1, padx=5, pady=5)
            
            row += 1
            
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        
        # # Tạo Label hiển thị tổng số mặt hàng và tổng số lượng
        self.total_item.set(TextNormalization.format_number(total_item_temp))
        self.total_quantity.set(TextNormalization.format_number(total_quantity_temp))
            
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
    
    def init_sub_frame(self):
        self.head_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.content_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.view_new_top_window = None
        
        # Sử dụng grid để đặt các Frame con trong frame_mat_hang
        self.head_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid(row=1, column=0, sticky="nsew")

        # Đặt trọng số cho các hàng và cột của frame_mat_hang để các Frame con thay đổi kích thước theo frame_mat_hang
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=3)
        self.frame.grid_columnconfigure(0, weight=1)
        
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
        
    def init_components(self):
        # ---- head_frame ----
        head_label = LabelType.h1(self.head_frame, TITLE_MAT_HANG) # Label trong head_frame
        head_label.grid(row=0, column=0, padx=5, pady=5)
        # Tạo ô nhập văn bản (Entry) cho tìm kiếm
        search_input_box = EntryType.blue(self.head_frame, text_var=self.search_var)
        search_input_box.grid(row=0, column=1, sticky="E", padx=5, pady=5)
        search_input_box.bind("<KeyRelease>", self.on_search) # Liên kết sự kiện nhập văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.head_frame, "Tìm kiếm")
        search_button.config(command=partial(self.on_search_button_click))
        search_button.grid(row=0, column=2, sticky="w")
        # Tạo nút làm mới thanh tìm kiếm
        refresh_button = ButtonType.brown(self.head_frame, "Làm mới tìm kiếm\nvà bảng dữ liệu")
        refresh_button.config(command=partial(self.refresh_entry_search))
        refresh_button.grid(row=0, column=3, sticky="w")
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_box = Listbox(self.head_frame, font=FontType.normal(), height=5, width=40)
        self.suggestion_box.grid(row=1, column=1, columnspan=2, sticky='nw')
        self.suggestion_box.bind("<<ListboxSelect>>", self.on_suggestion_select)
        # export and import 
        button_export = ButtonType.success(self.head_frame, "Xuất Excel")
        button_export.grid(row=1, column=3, sticky="nw")
        button_export.config(command=partial(self.export_data))
        button_import = ButtonType.primary(self.head_frame, "Nhập Excel")
        button_import.grid(row=1, column=3, sticky="w")
        button_import.config(command=partial(self.import_data))
        
        # button add
        button_add = ButtonType.success(self.head_frame, "Thêm mặt hàng")
        button_add.config(command=partial(self.view_add_item))
        button_add.grid(row=2, column=0, padx=5, pady=5)
        # Tạo Combobox cho chức năng sắp xếp
        label_sort = LabelType.normal_blue_white(self.head_frame, "Sắp xếp theo:")
        label_sort.grid(row=2, column=1, sticky="e", padx=5, pady=5)
        sort_combobox = ttk.Combobox(self.head_frame, textvariable=self.sort_var, font=FontType.normal())
        sort_combobox['values'] = self.mat_hang_service.get_mat_hang_sort_keys()
        sort_combobox.current(0)
        sort_combobox.grid(row=2, column=2, sticky="w")
        sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_selected) # Liên kết sự kiện chọn mục với hàm xử lý
        # ---- content_frame ----
        # Tạo Label hiển thị tổng số mặt hàng và tổng số lượng
        total_item_label = LabelType.normal_blue_white(self.head_frame, "Tổng mặt hàng:")
        total_item_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        total_item_view = EntryType.view(self.head_frame, text_var=self.total_item)
        total_item_view.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        total_quantity_label = LabelType.normal_blue_white(self.head_frame, "Tổng số lượng:")
        total_quantity_label.grid(row=3, column=2, sticky="e", padx=5, pady=5)
        total_quantity_view = EntryType.view(self.head_frame, text_var=self.total_quantity)
        total_quantity_view.grid(row=3, column=3, sticky="w", padx=5, pady=5)
        
    def show_column_title(self):
        for j in self.column_title:
            label = LabelType.title(self.scrollable_frame, text=j)
            label.grid(row=0, column=self.column_title.index(j), padx=5)
        
    def view_edit_item(self, mat_hang: MatHang):
        mat_hang = mat_hang.to_dict()
        self.view_new_top_window = Toplevel(self.parent)
        self.view_new_top_window.title('Xem chi tiết / Sửa')
        
        row = 1
        for key, value in MAT_HANG_COLUMN_NAMES.items():
            self.mat_hang_vars[key] = StringVar(self.view_new_top_window, value=mat_hang[key])
            if key == 'id' or key == 'ngay_tao':
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.view(self.view_new_top_window, text_var=self.mat_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            elif key == 'is_active':
                value = "Còn bán" if mat_hang[key] else "Ngừng bán"
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                Checkbutton(self.view_new_top_window, text="Còn bán", variable=self.mat_hang_vars[key], onvalue=True, offvalue=False).grid(row=row, column=1, padx=5, pady=5)  
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.mat_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        button_save = ButtonType.success(self.view_new_top_window, text="Lưu")
        button_save.config(command=partial(self.update, mat_hang_id=mat_hang["id"]))
        button_save.grid(row=row+1, column=0, padx=5, pady=5)
        
        button_exit = ButtonType.warning(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=row+1, column=1, padx=5, pady=5)
        
    def view_add_item(self):
        self.view_new_top_window = Toplevel(self.parent)
        self.view_new_top_window.title('Thêm mặt hàng')
        mat_hang = MatHang()
        mat_hang = mat_hang.to_dict()
        row = 1
        for key, value in MAT_HANG_COLUMN_NAMES.items():
            self.mat_hang_vars[key] = StringVar(self.view_new_top_window, value=mat_hang[key])
            if key == 'id' or key == 'ngay_tao':
                continue
            elif key == 'is_active':
                value = "Còn bán" if mat_hang[key] else "Ngừng bán"
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                Checkbutton(self.view_new_top_window, text="Còn bán", variable=self.mat_hang_vars[key], onvalue=True, offvalue=False).grid(row=row, column=1, padx=5, pady=5)  
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.mat_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
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
        
    def view_delete_item(self, mat_hang: dict):
        self.view_new_top_window = Toplevel(self.parent)
        self.view_new_top_window.title('Xóa mặt hàng')
        
        LabelType.h3(self.view_new_top_window, text=mat_hang['ten_hang']).grid(row=0, column=0, padx=5, pady=5)
        LabelType.normal(self.view_new_top_window, text="Bạn có chắc chắn muốn xóa mặt hàng này?").grid(row=1, column=0, padx=5, pady=5)

        button_delete = ButtonType.danger(self.view_new_top_window, text="Xóa")
        button_delete.config(command=partial(self.delete, mat_hang_id=mat_hang["id"]))
        button_delete.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        
        button_exit = ButtonType.info(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=2, column=0, padx=5, pady=5, sticky="E")
        
        