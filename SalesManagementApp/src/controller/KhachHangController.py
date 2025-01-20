import logging
from tkinter import Frame, StringVar, Toplevel, Checkbutton, Listbox, END
from tkinter import ttk
from contants import *
from templates.DataTableTemplate import DataTableTemplate
from static.css.ButtonType import ButtonType
from static.css.EntryType import EntryType
from static.css.FontType import FontType
from static.css.LabelType import LabelType
from src.entity.KhachHangEntity import KhachHang
from src.service.KhachHangService import KhachHangService
from src.utils.TextNormalization import TextNormalization
from functools import partial

class KhachHangController: # lấy data rồi đưa vào template
    def __init__(self, frame: Frame):
        logging.info("KhachHang Controller")
        self.frame = frame
        self.khach_hang_service = KhachHangService() # -------
        self.khach_hang_vars = {}  # Lưu trữ các StringVar để lấy giá trị sau này
        self.search_var = StringVar()
        self.suggestions = []
        self.total_item_label = None
        self.init_sub_frame() # ---Tạo các Frame con---
        self.init_table_data() # ---Tạo bảng dữ liệu---
        # ---- head_frame ----
        head_label = LabelType.h1(self.head_frame, TITLE_KHACH_HANG) # Label trong head_frame
        head_label.grid(row=0, column=0)
        # Tạo ô nhập văn bản (Entry) cho tìm kiếm
        search_input_box = EntryType.blue(self.head_frame, text_var=self.search_var)
        search_input_box.grid(row=0, column=1, sticky="E")
        search_input_box.bind("<KeyRelease>", self.on_search) # Liên kết sự kiện nhập văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.head_frame, "Tìm kiếm")
        search_button.config(command=partial(self.on_search_button_click))
        search_button.grid(row=0, column=2, sticky="w")
        # Tạo nút làm mới thanh tìm kiếm
        refresh_button = ButtonType.brown(self.head_frame, "Làm mới thanh tìm kiếm")
        refresh_button.config(command=partial(self.refresh_entry_search))
        refresh_button.grid(row=0, column=2)
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_box = Listbox(self.head_frame, font=FontType.normal(), height=5)
        self.suggestion_box.grid(row=1, column=1, sticky="E")
        self.suggestion_box.bind("<<ListboxSelect>>", self.on_suggestion_select)
        # button add
        button_add = ButtonType.success(self.head_frame, "Thêm khách hàng")
        button_add.config(command=partial(self.view_add_item))
        button_add.grid(row=2, column=0)
        # Tạo Combobox cho chức năng sắp xếp
        label_sort = LabelType.normal_blue_white(self.head_frame, "Sắp xếp theo:")
        label_sort.grid(row=2, column=1, sticky="nw")
        self.sort_var = StringVar()
        sort_combobox = ttk.Combobox(self.head_frame, textvariable=self.sort_var, font=FontType.normal())
        sort_combobox['values'] = self.khach_hang_service.get_khach_hang_sort_keys()
        sort_combobox.current(0)
        sort_combobox.grid(row=2, column=1, sticky="W")
        # Liên kết sự kiện chọn mục với hàm xử lý
        sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_selected)
        # ---- content_frame ----
        self.coloumn_title = list(KHACH_HANG_COLUMN_NAMES.values())
        self.coloumn_title.insert(0, "STT")
        
        self.refresh_khach_hang_list()

    def get_all(self):
        logging.info("Get all KhachHang")
        try:
            sort = self.sort_var.get()
            keyword = self.search_var.get()
            return self.khach_hang_service.get_all(sort=sort, keyword=keyword)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return []

    def get_by_id(self, khach_hang_id):
        logging.info("Get KhachHang with id: %s", khach_hang_id)
        try:
            khach_hang = self.khach_hang_service.get_by_id(khach_hang_id)
            self.view_edit_item(khach_hang)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
            return None

    def create(self):
        logging.info("Create KhachHang")
        khach_hang_data = {key: var.get() for key, var in self.khach_hang_vars.items()}
        khach_hang = KhachHang(**khach_hang_data)
        try: 
            self.khach_hang_service.create(khach_hang)
            print("Create KhachHang:", khach_hang.to_list())
            self.view_new_top_window.destroy()
            self.khach_hang_vars.clear()
            self.refresh_khach_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
    def create_and_continue(self):
        logging.info("Create and continue KhachHang")
        khach_hang_data = {key: var.get() for key, var in self.khach_hang_vars.items()}
        khach_hang = KhachHang(**khach_hang_data)
        try:
            self.khach_hang_service.create(khach_hang)
            print("Create and continue KhachHang:", khach_hang.to_list())
            self.view_new_top_window.destroy()
            self.khach_hang_vars.clear()
            self.refresh_khach_hang_list()
            self.view_add_item()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)

    def update(self, khach_hang_id):
        logging.info("Update KhachHang with id: %s", khach_hang_id)
        khach_hang_data = {key: var.get() for key, var in self.khach_hang_vars.items()}
        khach_hang = KhachHang(**khach_hang_data)
        try: 
            self.khach_hang_service.update(khach_hang_id, khach_hang)
            print("Update KhachHang with", khach_hang.to_list())
            self.view_new_top_window.destroy()
            self.khach_hang_vars.clear()
            self.refresh_khach_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)

    def delete(self, khach_hang_id):
        logging.info("Delete KhachHang with id: %s", id)
        try:
            self.khach_hang_service.delete(khach_hang_id)
            print(f"Delete KhachHang with id: {khach_hang_id}")
            self.view_new_top_window.destroy()
            self.refresh_khach_hang_list()
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error: %s", e)
        
    # --- Các hàm xử lý sự kiện ---
    # Hàm xử lý sự kiện nhập văn bản
    def on_search(self, event):
        search_text = self.search_var.get()
        print(f"Tìm kiếm: {search_text}", event)
        if search_text is not None and search_text.strip() != "":
            self.update_suggestions()
                  
    # Cập nhật danh sách gợi ý khi người dùng nhập từ khóa
    def update_suggestions(self, *args):
        keyword = self.search_var.get()
        print(f"Đang tìm kiếm gợi ý cho từ khóa: {keyword}")
        self.suggestions = self.khach_hang_service.get_suggestions(keyword)
        self.suggestion_box.delete(0, END)
        for suggestion in self.suggestions:
            self.suggestion_box.insert(END, suggestion)
        print(f"Gợi ý: {self.suggestions}")
        
    # Hàm xử lý khi nhấn nút tìm kiếm
    def on_search_button_click(self):
        self.refresh_khach_hang_list()
        
    # Làm mới danh sách khách hàng
    def refresh_entry_search(self):
        self.search_var.set("")
        self.refresh_khach_hang_list()
        
    # Xử lý sự kiện khi người dùng chọn một gợi ý
    def on_suggestion_select(self, event):
        selected_index = self.suggestion_box.curselection()
        if selected_index:
            selected_text = self.suggestion_box.get(selected_index)
            self.search_var.set(selected_text)
            
    # Hàm xử lý khi chọn mục trong Combobox Sort
    def on_sort_selected(self, event):
        sort_option = self.sort_var.get()
        print(f"Sắp xếp theo: {sort_option}")
        self.refresh_khach_hang_list()
        
    # --- Các hàm giao diện  ---
    def refresh_khach_hang_list(self):
        '''Lấy dữ liệu từ database và cập nhật giao diện'''
        # Thêm nội dung vào content frame với Scrollbar
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
        if self.total_item_label is None:
            self.show_total_label()
        else:
            self.destroy_total_label()
            self.show_total_label()
            
        khach_hang_list = self.get_all()
        total_item = len(khach_hang_list)
        # add title for table
        self.show_column_title()
        # Thêm các Label và Button vào scrollable_frame
        row = 1
        for khach_hang in khach_hang_list:
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            coloumn = 1
            khach_hang = khach_hang.to_dict()
            for key in KHACH_HANG_COLUMN_NAMES.keys():
                value = khach_hang[key]
                if key == "is_active":
                    value = "Thân thiết" if value else "Tiềm năng"
                label = LabelType.normal(self.scrollable_frame, text=value)
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)

                label.grid(row=row, column=coloumn, padx=5, pady=5)
                coloumn += 1
                
            # Thêm nút "Xem chi tiết/Sửa"
            view_edit_button = ButtonType.primary(self.scrollable_frame, text="Xem / Sửa")
            view_edit_button.config(command=partial(self.get_by_id, khach_hang_id=khach_hang['id']))
            view_edit_button.grid(row=row, column=coloumn, padx=5, pady=5)
            # Thêm nút "Xóa"
            delete_button = ButtonType.danger(self.scrollable_frame, text="Xóa")
            delete_button.config(command=partial(self.view_delete_item, khach_hang=khach_hang))
            delete_button.grid(row=row, column=coloumn+1, padx=5, pady=5)
            
            row += 1
            
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        self.show_total_label(total_item)
        
    def view_edit_item(self, khach_hang: KhachHang):
        khach_hang = khach_hang.to_dict()
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xem chi tiết / Sửa')
        
        row = 1
        for key, value in KHACH_HANG_COLUMN_NAMES.items():
            self.khach_hang_vars[key] = StringVar(self.view_new_top_window, value=khach_hang[key])
            if key == 'id' or key == 'ngay_tao':
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.view(self.view_new_top_window, text_var=self.khach_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            elif key == 'is_active':
                value = "Thân thiết" if khach_hang[key] else "Tiềm năng"
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                Checkbutton(self.view_new_top_window, text="Thân thiết", variable=self.khach_hang_vars[key], onvalue=True, offvalue=False).grid(row=row, column=1, padx=5, pady=5)  
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.khach_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        button_save = ButtonType.success(self.view_new_top_window, text="Lưu")
        button_save.config(command=partial(self.update, khach_hang_id=khach_hang["id"]))
        button_save.grid(row=row+1, column=0, padx=5, pady=5)
        
        button_exit = ButtonType.warning(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=row+1, column=1, padx=5, pady=5)
        
    def view_add_item(self):
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Thêm khách hàng')
        khach_hang = KhachHang()
        khach_hang = khach_hang.to_dict()
        row = 1
        for key, value in KHACH_HANG_COLUMN_NAMES.items():
            self.khach_hang_vars[key] = StringVar(self.view_new_top_window, value=khach_hang[key])
            if key == 'id' or key == 'ngay_tao':
                continue
            elif key == 'is_active':
                value = "Thân thiết" if khach_hang[key] else "Tiềm năng"
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                Checkbutton(self.view_new_top_window, text="Thân thiết", variable=self.khach_hang_vars[key], onvalue=True, offvalue=False).grid(row=row, column=1, padx=5, pady=5)  
            else: 
                LabelType.normal_blue_white(self.view_new_top_window, text=value).grid(row=row, column=0, padx=5, pady=5)
                EntryType.normal(self.view_new_top_window, text_var=self.khach_hang_vars[key]).grid(row=row, column=1, padx=5, pady=5)
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
        
    def view_delete_item(self, khach_hang: dict):
        self.view_new_top_window = Toplevel(self.frame)
        self.view_new_top_window.title('Xóa khách hàng')
        
        LabelType.h3(self.view_new_top_window, text=khach_hang['ten_khach_hang']).grid(row=0, column=0, padx=5, pady=5)
        LabelType.normal(self.view_new_top_window, text="Bạn có chắc chắn muốn xóa khách hàng này?").grid(row=1, column=0, padx=5, pady=5)

        button_delete = ButtonType.danger(self.view_new_top_window, text="Xóa")
        button_delete.config(command=partial(self.delete, khach_hang_id=khach_hang["id"]))
        button_delete.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        
        button_exit = ButtonType.info(self.view_new_top_window, text="Thoát")
        button_exit.config(command=partial(self.view_new_top_window.destroy))
        button_exit.grid(row=2, column=0, padx=5, pady=5, sticky="E")
    
    def show_column_title(self):
        for j in self.coloumn_title:
            label = LabelType.title(self.scrollable_frame, text=j)
            label.grid(row=0, column=self.coloumn_title.index(j), padx=5)
            
    def show_total_label(self, total_item=0):
        self.total_item_label = LabelType.h4(self.head_frame, f"Tổng khách hàng: {TextNormalization.format_number(total_item)}", text_color=TEXT_COLOR_BLUE)
        self.total_item_label.grid(row=2, column=2, sticky="W")
        
    def destroy_total_label(self):
        self.total_item_label.destroy()
        
    def init_sub_frame(self):
        self.head_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.content_frame = Frame(self.frame, bg=BG_COLOR_FRAME_WHITE, relief="sunken")
        self.view_new_top_window = None
        # Sử dụng grid để đặt các Frame con trong frame_khach_hang
        self.head_frame.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        # Đặt trọng số cho các hàng và cột của frame_khach_hang để các Frame con thay đổi kích thước theo frame_khach_hang
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