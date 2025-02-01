import logging
from tkinter import Frame, StringVar, Toplevel, Listbox, END
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
        self.nhap_hang_service = NhapHangService() 
        self.nhap_hang_list_var = []
        self.search_mat_hang_var = StringVar()
        self.view_cancel_top_window = None
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
        search_text = self.search_mat_hang_var.get()
        if search_text is not None and search_text.strip() != "":
            suggestions = self.nhap_hang_service.search_mat_hang(search_text)
            self.suggestion_mat_hang_box.delete(0, END)
            for suggestion in suggestions:
                text = suggestion.get('id') + " - " + suggestion.get('ten_hang') + " - " + suggestion.get('don_vi')
                self.suggestion_mat_hang_box.insert(END, text)
    
    #  Hàm xử lý sự kiện khi chọn hàng hóa từ gợi ý
    def on_suggestion_mat_hang_select(self, event):
        selected_index = self.suggestion_mat_hang_box.curselection()
        if selected_index:
            selected_text = self.suggestion_mat_hang_box.get(selected_index)
            # self.search_mat_hang_var.set(selected_text)
            text_arr = str(selected_text).split(" - ")
            nhap_hang = NhapHang(id_mat_hang=text_arr[0], ten_hang=text_arr[1], don_vi=text_arr[2])
            nhap_hang_var = {}
            for key, value in nhap_hang.to_dict().items():
                nhap_hang_var[key] = StringVar(value=value)
            self.nhap_hang_list_var.append(nhap_hang_var)
            self.refresh_nhap_hang_list()
    
    #  Hàm xử lý sự kiện khi nhấn nút tìm kiếm hàng hóa
    def on_search_mat_hang_button_click(self):
        pass
    
    #  Hàm xử lý sự kiện khi nhập văn bản tìm kiếm nhà cung cấp
    def on_search_ncc(self, event):
        search_text = self.search_ncc_var.get()
        if search_text is not None and search_text.strip() != "":
            suggestions = self.nhap_hang_service.search_ncc(search_text)
            self.suggestion_ncc_box.delete(0, END)
            for suggestion in suggestions:
                self.suggestion_ncc_box.insert(END, suggestion)
    
    #  Hàm xử lý sự kiện khi chọn nhà cung cấp từ gợi ý
    def on_suggestion_ncc_select(self, event):
        selected_index = self.suggestion_ncc_box.curselection()
        if selected_index:
            selected_text = self.suggestion_ncc_box.get(selected_index)
            self.search_ncc_var.set(selected_text)
    
    #  Hàm xử lý sự kiện khi nhấn nút tìm kiếm nhà cung cấp
    def on_search_ncc_button_click(self):
        pass
    
    def save_all(self):
        from src.controller.NhapHangController import NhapHangController
        for nhap_hang_var in self.nhap_hang_list_var:
            nhap_hang_data = {key: var.get() for key, var in nhap_hang_var.items()}
            nhap_hang = NhapHang(**nhap_hang_data)
            self.nhap_hang_service.create(nhap_hang)
        NhapHangController(self.frame)
    
    def delete_hang_nhap(self, index):
        self.nhap_hang_list_var.pop(index)
        self.refresh_nhap_hang_list()
    
    #  hàm xử lý giao diện khi chọn hàng hóa từ gợi ý
    def refresh_nhap_hang_list(self):
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
        self.show_column_title()
        row = 1
        total_nhap_hang_temp = len(self.nhap_hang_list_var)
        total_so_luong_temp = 0
        total_thanh_tien_temp = 0
        for i, nhap_hang_var in enumerate(self.nhap_hang_list_var):
            so_luong = str(nhap_hang_var.get('so_luong').get()).strip()
            gia_nhap = str(nhap_hang_var.get('gia_nhap').get()).strip()
            if so_luong is not None and str(so_luong).isdigit():
                so_luong = int(so_luong)
            else:
                so_luong = 0
            if gia_nhap is not None and str(gia_nhap).isdigit():
                gia_nhap = int(gia_nhap)
            else:
                gia_nhap = 0
            total_so_luong_temp += so_luong
            total_thanh_tien_temp += so_luong * gia_nhap
            nhap_hang_var.get('thanh_tien').set(str(so_luong * gia_nhap))
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            coloumn = 1
            for key in NHAP_HANG_COLUMN_NAMES.keys():
                if key == 'id' or key == 'ngay_nhap' or key == 'id_mat_hang':
                    continue
                elif key == 'ten_hang' or key == 'id' or key == 'don_vi':
                    label = LabelType.normal(self.scrollable_frame, text=nhap_hang_var.get(key).get())
                    label.grid(row=row, column=coloumn, padx=5, pady=5)
                elif key == 'thanh_tien':
                    label = LabelType.normal(self.scrollable_frame, text=TextNormalization.format_number(nhap_hang_var.get(key).get()) + f" {MONEY_UNIT}")
                    label.grid(row=row, column=coloumn, padx=5, pady=5)
                else:
                    entry = EntryType.normal(self.scrollable_frame, text_var=nhap_hang_var.get(key))
                    entry.grid(row=row, column=coloumn, padx=5, pady=5)
                coloumn += 1
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)
            button_delete = ButtonType.danger(self.scrollable_frame, "Xóa")
            button_delete.grid(row=row, column=coloumn, padx=5, pady=5)
            button_delete.config(command=partial(self.delete_hang_nhap, i))
            row += 1
            
            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar_y.pack(side="right", fill="y")

            self.total_nhap_hang.set(TextNormalization.format_number(total_nhap_hang_temp))
            self.total_so_luong.set(TextNormalization.format_number(total_so_luong_temp))
            self.total_thanh_tien.set(TextNormalization.format_number(total_thanh_tien_temp) + f" {MONEY_UNIT}")
    
    def destroy_all_by_cancel(self):
        from src.controller.NhapHangController import NhapHangController
        self.view_cancel_top_window.destroy()
        NhapHangController(self.frame)
    
    def view_cancel(self):
        self.view_cancel_top_window = Toplevel(self.frame)
        self.view_cancel_top_window.title("Hủy nhập hàng")
        self.view_cancel_top_window.rowconfigure(0, weight=1)
        self.view_cancel_top_window.rowconfigure(1, weight=1)
        self.view_cancel_top_window.columnconfigure(0, weight=1)
        self.view_cancel_top_window.geometry("400x200")
        self.view_cancel_top_window.grab_set()
        LabelType.h4(self.view_cancel_top_window, "Bạn có chắc chắn muốn hủy nhập hàng không?").grid(row=0, column=0)
        button_yes = ButtonType.danger(self.view_cancel_top_window, "Xác nhận")
        button_yes.grid(row=1, column=0, sticky="w", padx=10)
        button_yes.config(command=partial(self.destroy_all_by_cancel))
        button_no = ButtonType.primary(self.view_cancel_top_window, "Không")
        button_no.grid(row=1, column=0, sticky="e", padx=10)
        button_no.config(command=self.view_cancel_top_window.destroy)
        
    def show_column_title(self):
        column = 0
        for j in self.coloumn_title:
            if j == 'Mã nhập hàng' or j == 'Ngày nhập' or j == 'Mã hàng':
                continue
            label = LabelType.title(self.scrollable_frame, text=j)
            label.grid(row=0, column=column, padx=5)
            column += 1
        
    def init_sub_frame(self):
        self.sub_frame_top = Frame(self.frame, bg=BG_COLOR_LIGHT_BLUE, relief="sunken")
        self.sub_frame_top.grid(row=0, column=0, sticky="nsew", padx=10)
        self.sub_frame_bottom = Frame(self.frame, bg=BG_COLOR_LIGHT_GRAY, relief="sunken")
        self.sub_frame_bottom.grid(row=1, column=0, sticky="nsew", padx=10)
        
        self.sub_frame_bottom_top = Frame(self.sub_frame_bottom)
        self.sub_frame_bottom_top.grid(row=0, column=0, sticky="nsew")
        self.sub_frame_bottom_middle = Frame(self.sub_frame_bottom)
        self.sub_frame_bottom_middle.grid(row=1, column=0, sticky="nsew")
        self.sub_frame_bottom_bottom = Frame(self.sub_frame_bottom)
        self.sub_frame_bottom_bottom.grid(row=2, column=0, sticky="nsew")
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=4)
        self.frame.columnconfigure(0, weight=1)
        self.sub_frame_bottom.rowconfigure(0, weight=1)
        self.sub_frame_bottom.rowconfigure(1, weight=2)
        self.sub_frame_bottom.rowconfigure(2, weight=1)
        self.sub_frame_bottom.columnconfigure(0, weight=1)
        
        self.sub_frame_bottom_top.rowconfigure(0, weight=1)
        self.sub_frame_bottom_top.rowconfigure(1, weight=1)
        self.sub_frame_bottom_top.columnconfigure(0, weight=1)
        self.sub_frame_bottom_top.columnconfigure(1, weight=1)
        self.sub_frame_bottom_top.columnconfigure(2, weight=1)
        self.sub_frame_bottom_top.columnconfigure(3, weight=1)
        
        self.sub_frame_bottom_bottom.rowconfigure(0, weight=1)
        self.sub_frame_bottom_bottom.columnconfigure(0, weight=1)
        self.sub_frame_bottom_bottom.columnconfigure(1, weight=1)
        
        self.sub_frame_top.rowconfigure(0, weight=1)
        self.sub_frame_top.rowconfigure(1, weight=1)
        self.sub_frame_top.columnconfigure(0, weight=1)
        self.sub_frame_top.columnconfigure(1, weight=1)
        self.sub_frame_top.columnconfigure(2, weight=1)
        self.sub_frame_top.columnconfigure(3, weight=1)
        
        
    def init_components(self):
        # ---- sub_frame_bottom_top ----
        head_label = LabelType.h1(self.sub_frame_bottom_top, "Thêm nhập hàng") # Label trong head_frame
        head_label.grid(row=0, column=0, padx=5, pady=5)
        button_refresh = ButtonType.brown(self.sub_frame_bottom_top, "Làm mới dữ liệu")
        button_refresh.grid(row=0, column=1, padx=5, pady=5)
        button_refresh.config(command=partial(self.refresh_nhap_hang_list))
        total_nhap_hang_label = LabelType.normal_blue_white(self.sub_frame_bottom_top, text="Tổng nhập hàng:")
        total_nhap_hang_label.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        total_nhap_hang_value = EntryType.view(self.sub_frame_bottom_top, text_var=self.total_nhap_hang)
        total_nhap_hang_value.grid(row=0, column=3, sticky='w', padx=5, pady=5)
        total_so_luong_label = LabelType.normal_blue_white(self.sub_frame_bottom_top, text="Tổng số lượng:")
        total_so_luong_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        total_so_luong_value = EntryType.view(self.sub_frame_bottom_top, text_var=self.total_so_luong)
        total_so_luong_value.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        total_thanh_tien_label = LabelType.normal_blue_white(self.sub_frame_bottom_top, text="Tổng thành tiền:")
        total_thanh_tien_label.grid(row=1, column=2, sticky='e', padx=5, pady=5)
        total_thanh_tien_value = EntryType.view(self.sub_frame_bottom_top, text_var=self.total_thanh_tien)
        total_thanh_tien_value.grid(row=1, column=3, sticky='w', padx=5, pady=5)
        
        # ---- sub_frame_bottom_bottom ----
        button_add = ButtonType.success(self.sub_frame_bottom_bottom, "Lưu toàn bộ nhập hàng")
        button_add.config(command=partial(self.save_all))
        button_add.grid(row=0, column=0, padx=5, pady=5)
        button_cancel = ButtonType.danger(self.sub_frame_bottom_bottom, "Hủy")
        button_cancel.config(command=partial(self.view_cancel))
        button_cancel.grid(row=0, column=1, padx=5, pady=5)
        
        # Tạo ô nhập văn bản (Entry) cho tìm kiếm hàng hóa
        search_input_box = EntryType.blue(self.sub_frame_top, text_var=self.search_mat_hang_var)
        search_input_box.grid(row=0, column=0, sticky='se', pady=5)
        search_input_box.bind("<KeyRelease>", self.on_search_mat_hang) # Liên kết sự kiện nhập văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.sub_frame_top, "Tìm kiếm mặt hàng")
        search_button.config(command=partial(self.on_search_mat_hang_button_click))
        search_button.grid(row=0, column=1, sticky='sw', padx=5)
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_mat_hang_box = Listbox(self.sub_frame_top, font=FontType.normal(), height=10, width=50)
        self.suggestion_mat_hang_box.grid(row=1, column=0, columnspan=2)
        self.suggestion_mat_hang_box.bind("<<ListboxSelect>>", self.on_suggestion_mat_hang_select)
        
        # Tạo ô nhập văn bản (Entry) cho tìm kiếm ncc
        search_input_box = EntryType.blue(self.sub_frame_top, text_var=self.search_ncc_var)
        search_input_box.grid(row=0, column=2, sticky='se', pady=5)
        search_input_box.bind("<KeyRelease>", self.on_search_ncc) # Liên kết sự kiện nhập văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.sub_frame_top, "Tìm kiếm nhà cung cấp")
        search_button.config(command=partial(self.on_search_ncc_button_click))
        search_button.grid(row=0, column=3, sticky='sw', padx=5)
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_ncc_box = Listbox(self.sub_frame_top, font=FontType.normal(), height=10, width=50)
        self.suggestion_ncc_box.grid(row=1, column=2, columnspan=2)
        self.suggestion_ncc_box.bind("<<ListboxSelect>>", self.on_suggestion_ncc_select)
        
    def init_table_data(self):
        data_table = DataTableTemplate(self.sub_frame_bottom_middle)
        self.canvas = data_table.get_canvas()
        self.scrollbar_y = data_table.get_scrollbar_y()
        self.scrollbar_x = data_table.get_scrollbar_x()
        self.scrollable_frame = data_table.get_scrollable_frame()
        
    def destroy_table_data(self):
        self.canvas.destroy()
        self.scrollbar_y.destroy()
        self.scrollbar_x.destroy()
        self.scrollable_frame.destroy()
        
