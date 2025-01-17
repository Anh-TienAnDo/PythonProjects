import logging
from tkinter import Frame, StringVar, Toplevel, Checkbutton
from tkinter import ttk
from contants import *
from templates.DataTableTemplate import DataTableTemplate
from static.css.ButtonType import ButtonType
from static.css.EntryType import EntryType
from static.css.FontType import FontType
from static.css.LabelType import LabelType
from src.entity.MatHangEntity import MatHang
from src.service.MatHangService import MatHangService
from functools import partial


class MatHangController: # lấy data rồi đưa vào template
    def __init__(self, frame: Frame):
        logging.info("MatHang Controller")
        self.mat_hang_service = MatHangService()
        self.frame = frame
        # Tạo các Frame con
        self.head_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.content_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.view_new_top_window = None
        self.mat_hang_vars = {}  # Lưu trữ các StringVar để lấy giá trị sau này
        # đặt các Frame
        self.grid_sub_frame()
        
        # ---- head_frame ----
        # Tạo Label trong head_frame
        head_label = LabelType.h1(self.head_frame, TITLE_MAT_HANG)
        head_label.grid(row=0, column=0)
        
        # search function
        self.search_var = StringVar()
        search_input_box = EntryType.blue(self.head_frame, text_var=self.search_var)
        search_input_box.grid(row=0, column=11)
        # Liên kết sự kiện nhập văn bản với hàm xử lý
        search_input_box.bind("<KeyRelease>", self.on_search)
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.head_frame, "Tìm kiếm")
        search_button.config(command=partial(self.on_search_button_click))
        search_button.grid(row=0, column=12)
        
        # button add
        button_add = ButtonType.success(self.head_frame, "Thêm mặt hàng")
        button_add.config(command=partial(self.view_add_item))
        button_add.grid(row=1, column=0)
        
        # Tạo Combobox cho chức năng sắp xếp
        label_sort = LabelType.normal_blue_white(self.head_frame, "Sắp xếp theo:")
        label_sort.grid(row=1, column=1)
        self.sort_var = StringVar()
        sort_combobox = ttk.Combobox(self.head_frame, textvariable=self.sort_var, font=FontType.normal())
        sort_combobox['values'] = self.mat_hang_service.get_mat_hang_sort_keys()
        sort_combobox.current(0)
        sort_combobox.grid(row=1, column=2)
        # Liên kết sự kiện chọn mục với hàm xử lý
        sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_selected)
        
        # data, total item + total quantity
        # self.mat_hang_list = []
        self.coloumn_title = list(MAT_HANG_COLUMN_NAMES.values())
        self.coloumn_title.insert(0, "STT")
        
        self.init_table_data()
        self.refresh_mat_hang_list()

# chech search, filter -> refresh data -> get data
    def get_all(self) -> list[MatHang]:
        logging.info("Get all MatHang")
        try:
            sort = self.sort_var.get()
            return self.mat_hang_service.get_all(sort=sort)
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
            print("Create MatHang:", mat_hang.to_list())
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
            print("Create and continue MatHang:", mat_hang.to_list())
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
            print(f"Update MatHang with", mat_hang.to_list())
            self.view_new_top_window.destroy()
            self.mat_hang_vars.clear()
            self.refresh_mat_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)

    def delete(self, mat_hang_id: str):
        logging.info("Delete MatHang with id: %s", mat_hang_id)
        try:
            # self.mat_hang_service.delete(mat_hang_id)
            print(f"Delete MatHang with id: {mat_hang_id}")
            self.refresh_mat_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
    # Hàm xử lý sự kiện nhập văn bản
    def on_search(self, event):
        search_text = self.search_var.get()
        print(f"Tìm kiếm: {search_text}", event)
        # Thực hiện tìm kiếm và cập nhật giao diện tại đây

    # Hàm xử lý khi nhấn nút tìm kiếm
    def on_search_button_click(self):
        search_text = self.search_var.get()
        print(f"Nút tìm kiếm được nhấn. Tìm kiếm: {search_text}")
        # Thực hiện tìm kiếm và cập nhật giao diện tại đây
        
    # Hàm xử lý khi chọn mục trong Combobox
    def on_sort_selected(self, event):
        sort_option = self.sort_var.get()
        print(f"Sắp xếp theo: {sort_option}")
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
        total_item = len(mat_hang_list)
        total_quantity = 0
        # add title for table
        self.show_column_title()

        # Thêm các Label và Button vào scrollable_frame
        row = 1
        for mat_hang in mat_hang_list:
            total_quantity += mat_hang.so_luong
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            coloumn = 1
            mat_hang = mat_hang.to_dict()
            for key in MAT_HANG_COLUMN_NAMES.keys():
                value = mat_hang[key]
                if key == "is_active":
                    value = "Còn bán" if value else "Không bán"
                label = LabelType.normal(self.scrollable_frame, text=value)
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)

                label.grid(row=row, column=coloumn, padx=5, pady=5)
                coloumn += 1
                
            # Thêm nút "Xem chi tiết/Sửa"
            view_edit_button = ButtonType.primary(self.scrollable_frame, text="Xem / Sửa")
            view_edit_button.config(command=partial(self.get_by_id, mat_hang_id=mat_hang['id']))
            view_edit_button.grid(row=row, column=coloumn, padx=5, pady=5)

            # Thêm nút "Xóa"
            delete_button = ButtonType.danger(self.scrollable_frame, text="Xóa")
            delete_button.config(command=partial(self.delete, mat_hang_id=mat_hang['id']))
            delete_button.grid(row=row, column=coloumn+1, padx=5, pady=5)
            
            row += 1
            
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        
        # Tạo Label hiển thị tổng số mặt hàng và tổng số lượng
        self.show_total_label(total_item, total_quantity)
            
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
    
    def grid_sub_frame(self):
        # Sử dụng grid để đặt các Frame con trong frame_mat_hang
        self.head_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.content_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Đặt trọng số cho các hàng và cột của frame_mat_hang để các Frame con thay đổi kích thước theo frame_mat_hang
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=3)
        self.frame.grid_columnconfigure(0, weight=1)
        
    def show_column_title(self):
        for j in self.coloumn_title:
            label = LabelType.h4(self.scrollable_frame, text=j)
            label.grid(row=0, column=self.coloumn_title.index(j))
            
    def show_total_label(self, total_item, total_quantity):
        total_item_label = LabelType.normal_blue_white(self.head_frame, f"Tổng số mặt hàng: {total_item}")
        total_quantity_label = LabelType.normal_blue_white(self.head_frame, f"Tổng số lượng: {total_quantity}")
        total_item_label.grid(row=1, column=3)
        total_quantity_label.grid(row=1, column=4)
        
    def view_edit_item(self, mat_hang: MatHang):
        mat_hang = mat_hang.to_dict()
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xem chi tiết / Sửa')
        
        row = 1
        for key, value in MAT_HANG_COLUMN_NAMES.items():
            self.mat_hang_vars[key] = StringVar(self.view_new_top_window, value=mat_hang[key])
            if key == 'id' or key == 'ngay_tao':
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.view(self.view_new_top_window, text_var=self.mat_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            elif key == 'is_active':
                value = "Còn bán" if mat_hang[key] else "Không bán"
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
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Thêm mặt hàng')
        mat_hang = MatHang()
        mat_hang = mat_hang.to_dict()
        row = 1
        for key, value in MAT_HANG_COLUMN_NAMES.items():
            self.mat_hang_vars[key] = StringVar(self.view_new_top_window, value=mat_hang[key])
            if key == 'id' or key == 'ngay_tao':
                continue
            elif key == 'is_active':
                value = "Còn bán" if mat_hang[key] else "Không bán"
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                Checkbutton(self.view_new_top_window, text="Còn bán", variable=self.mat_hang_vars[key], onvalue=True, offvalue=False).grid(row=row, column=1, padx=5, pady=5)  
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.mat_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        button_add = ButtonType.success(self.view_new_top_window, text="Thêm & tiếp")
        button_add.config(command=partial(self.create_and_continue))
        button_add.grid(row=row+1, column=0, padx=5, pady=5)
        
        button_save = ButtonType.primary(self.view_new_top_window, text="Lưu")
        button_save.config(command=partial(self.create))
        button_save.grid(row=row+1, column=1, padx=5, pady=5)
        
        button_exit = ButtonType.warning(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=row+1, column=2, padx=5, pady=5)
        
    def view_delete_item(self, mat_hang: MatHang):
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xóa mặt hàng')
        
        LabelType.h3(self.view_new_top_window, text=mat_hang.ten_hang).grid(row=0, column=0, padx=5, pady=5)
        LabelType.h4(self.view_new_top_window, text="Bạn có chắc chắn muốn xóa mặt hàng này?").grid(row=1, column=0, padx=5, pady=5)

        button_delete = ButtonType.danger(self.view_new_top_window, text="Xóa")
        button_delete.config(command=partial(self.delete, mat_hang_id=mat_hang["id"]))
        button_delete.grid(row=2, column=0, padx=5, pady=5)
        
        button_exit = ButtonType.normal(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=2, column=1, padx=5, pady=5)
        
        