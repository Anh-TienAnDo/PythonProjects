import logging
from tkinter import Frame, StringVar, Toplevel, Listbox, END, messagebox, filedialog
from contants import *
from templates.DataTableTemplate import DataTableTemplate
from static.css.ButtonType import ButtonType
from static.css.EntryType import EntryType
from static.css.FontType import FontType
from static.css.LabelType import LabelType
from src.entity.BanHangEntity import BanHang
from src.service.BanHangService import BanHangService
from src.utils.TextNormalization import TextNormalization
from functools import partial
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class BanHangAddController:
    def __init__(self, frame: Frame):
        self.frame = frame
        logging.info("BanHangAdd Controller")
        self.ban_hang_service = BanHangService() 
        self.ban_hang_list_var = []
        self.search_mat_hang_var = StringVar()
        self.view_cancel_top_window = None
        self.search_khach_hang_var = StringVar()
        self.total_ban_hang = StringVar()
        self.total_so_luong = StringVar()
        self.total_thanh_tien = StringVar()
        self.selected_folder = None
        self.coloumn_title = list(BAN_HANG_COLUMN_NAMES.values())
        self.coloumn_title.insert(0, "STT")
        
        self.init_sub_frame() # ---Tạo các Frame con---
        self.init_table_data() # ---Tạo bảng dữ liệu---
        self.init_components() # ---Tạo các thành phần giao diện---
        # ---- content_frame ----
        self.refresh_ban_hang_list()
        
    #  Hàm xử lý sự kiện khi bán văn bản tìm kiếm hàng hóa
    def on_search_mat_hang(self, event):
        search_text = self.search_mat_hang_var.get()
        if search_text is not None and search_text.strip() != "":
            suggestions = self.ban_hang_service.search_mat_hang(search_text)
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
            ban_hang = BanHang(id_mat_hang=text_arr[0], ten_hang=text_arr[1], don_vi=text_arr[2])
            ban_hang_var = {}
            for key, value in ban_hang.to_dict().items():
                ban_hang_var[key] = StringVar(value=value)
            self.ban_hang_list_var.append(ban_hang_var)
            self.refresh_ban_hang_list()
    
    #  Hàm xử lý sự kiện khi nhấn nút tìm kiếm hàng hóa
    def on_search_mat_hang_button_click(self):
        pass
    
    #  Hàm xử lý sự kiện khi bán văn bản tìm kiếm khách hàng
    def on_search_khach_hang(self, event):
        search_text = self.search_khach_hang_var.get()
        if search_text is not None and search_text.strip() != "":
            suggestions = self.ban_hang_service.search_khach_hang(search_text)
            self.suggestion_khach_hang_box.delete(0, END)
            for suggestion in suggestions:
                self.suggestion_khach_hang_box.insert(END, suggestion)
    
    #  Hàm xử lý sự kiện khi chọn khách hàng từ gợi ý
    def on_suggestion_khach_hang_select(self, event):
        selected_index = self.suggestion_khach_hang_box.curselection()
        if selected_index:
            selected_text = self.suggestion_khach_hang_box.get(selected_index)
            self.search_khach_hang_var.set(selected_text)
    
    #  Hàm xử lý sự kiện khi nhấn nút tìm kiếm khách hàng
    def on_search_khach_hang_button_click(self):
        pass
    
    def save_all(self):
        from src.controller.BanHangController import BanHangController
        for ban_hang_var in self.ban_hang_list_var:
            ban_hang_data = {key: var.get() for key, var in ban_hang_var.items()}
            ban_hang = BanHang(**ban_hang_data)
            self.ban_hang_service.create(ban_hang)
        BanHangController(self.frame)
        # self.view_new_top_window.destroy()
    
    def delete_hang_ban(self, index):
        self.ban_hang_list_var.pop(index)
        self.refresh_ban_hang_list()   
        
    def export_invoice(self):
        try:
            self.register_fonts()
            self.select_folder()
            invoice_data = {
                "Ngày bán": datetime.now().strftime("%d/%m/%Y"),
                "Những mặt hàng": [],
                "Tổng tiền": ""
            }
            total = 0
            for ban_hang_var in self.ban_hang_list_var:
                ban_hang_data = {key: str(var.get()).strip() for key, var in ban_hang_var.items()}
                item = {}
                thanh_tien = int(ban_hang_data.get('so_luong')) * int(ban_hang_data.get('gia_ban'))
                total += thanh_tien
                item['thanh_tien'] = TextNormalization.format_number(thanh_tien)
                for key, value in ban_hang_data.items():
                    if key == "ten_hang":
                        item["ten_hang"] = value
                    elif key == "so_luong":
                        item["so_luong"] = TextNormalization.format_number(value)
                    elif key == "gia_ban":
                        item["gia_ban"] = TextNormalization.format_number(value)
                invoice_data["Những mặt hàng"].append(item)
            invoice_data["Tổng tiền"] = TextNormalization.format_number(total)
            # Tạo tài liệu PDF
            pdf_filename = f"{self.selected_folder}/invoice_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
            self.create_invoice_pdf(pdf_filename, invoice_data)
            messagebox.showinfo("Xuất hóa đơn thành công", f"Đã xuất hóa đơn tại: {pdf_filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra: {e}")
            
    def select_folder(self):
        # Mở hộp thoại chọn thư mục
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            messagebox.showinfo("Thư mục đã chọn", f"Thư mục đã chọn: {folder_selected}")
            self.selected_folder = folder_selected
        else:
            messagebox.showwarning("Chưa chọn thư mục", "Bạn chưa chọn thư mục nào.")
    
    def create_invoice_pdf(self, filename, invoice_data):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        # Tiêu đề hóa đơn
        c.setFont("Arial", 20)
        c.drawString(200, height - 50, "HÓA ĐƠN BÁN HÀNG")
        # Thông tin hóa đơn
        c.setFont("Arial", 12)
        y = height - 100
        for key, value in invoice_data.items():
            if key != "Những mặt hàng":
                c.drawString(50, y, f"{key}: {value}")
                y -= 20
        # Thông tin sản phẩm
        c.drawString(50, y, "Sản phẩm:")
        y -= 20
        for item in invoice_data['Những mặt hàng']:
            c.drawString(70, y, f"Mặt hàng: {item['ten_hang']} - Số lượng: {item['so_luong']} - Giá: {item['gia_ban']} - Thành tiền: {item['thanh_tien']}")
            y -= 20
        # Tổng cộng
        c.drawString(50, y, f"Tổng cộng: {invoice_data['Tổng tiền']} {MONEY_UNIT}")
        c.save()
        
    #  hàm xử lý giao diện khi chọn hàng hóa từ gợi ý
    def refresh_ban_hang_list(self):
        if self.canvas is None:
            self.init_table_data()
        else:
            self.destroy_table_data()
            self.init_table_data()
        self.show_column_title()
        row = 1
        total_ban_hang_temp = len(self.ban_hang_list_var)
        total_so_luong_temp = 0
        total_thanh_tien_temp = 0
        for i, ban_hang_var in enumerate(self.ban_hang_list_var):
            so_luong = str(ban_hang_var.get('so_luong').get()).strip()
            gia_ban = str(ban_hang_var.get('gia_ban').get()).strip()
            if so_luong is not None and str(so_luong).isdigit():
                so_luong = int(so_luong)
            else:
                so_luong = 0
            if gia_ban is not None and str(gia_ban).isdigit():
                gia_ban = int(gia_ban)
            else:
                gia_ban = 0
            total_so_luong_temp += so_luong
            total_thanh_tien_temp += so_luong * gia_ban
            ban_hang_var.get('thanh_tien').set(str(so_luong * gia_ban))
            label_stt = LabelType.normal(self.scrollable_frame, text=str(row))
            if row % 2 == 0:
                label_stt.config(bg=BG_COLOR_LIGHT_BLUE)
            label_stt.grid(row=row, column=0, padx=5, pady=5)
            column = 1
            for key in BAN_HANG_COLUMN_NAMES.keys():
                if key == 'id' or key == 'id_mat_hang' or key == 'ngay_ban':
                    continue
                elif key == 'ten_hang' or key == 'id' or key == 'don_vi':
                    label = LabelType.normal(self.scrollable_frame, text=ban_hang_var.get(key).get())
                    label.grid(row=row, column=column, padx=5, pady=5)
                elif key == 'thanh_tien':
                    label = LabelType.normal(self.scrollable_frame, text=TextNormalization.format_number(ban_hang_var.get(key).get()) + f" {MONEY_UNIT}")
                    label.grid(row=row, column=column, padx=5, pady=5)
                else:
                    entry = EntryType.normal(self.scrollable_frame, text_var=ban_hang_var.get(key))
                    entry.grid(row=row, column=column, padx=5, pady=5)
                column += 1
                if row % 2 == 0:
                    label.config(bg=BG_COLOR_LIGHT_BLUE)
            button_delete = ButtonType.danger(self.scrollable_frame, "Xóa")
            button_delete.grid(row=row, column=column, padx=5, pady=5)
            button_delete.config(command=partial(self.delete_hang_ban, i))
            row += 1
            
            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar_y.pack(side="right", fill="y")

            self.total_ban_hang.set(TextNormalization.format_number(total_ban_hang_temp))
            self.total_so_luong.set(TextNormalization.format_number(total_so_luong_temp))
            self.total_thanh_tien.set(TextNormalization.format_number(total_thanh_tien_temp) + f" {MONEY_UNIT}")
    
    def destroy_all_by_cancel(self):
        self.view_cancel_top_window.destroy()
        from src.controller.BanHangController import BanHangController
        BanHangController(self.frame)
        # self.view_new_top_window.destroy()
    
    def view_cancel(self):
        self.view_cancel_top_window = Toplevel(self.frame)
        # self.view_cancel_top_window = Toplevel(self.view_new_top_window)
        self.view_cancel_top_window.title("Hủy đơn hàng")
        self.view_cancel_top_window.rowconfigure(0, weight=1)
        self.view_cancel_top_window.rowconfigure(1, weight=1)
        self.view_cancel_top_window.columnconfigure(0, weight=1)
        self.view_cancel_top_window.geometry("400x200")
        self.view_cancel_top_window.grab_set()
        LabelType.h4(self.view_cancel_top_window, "Bạn có chắc chắn muốn hủy đơn hàng không?").grid(row=0, column=0)
        button_yes = ButtonType.danger(self.view_cancel_top_window, "Xác nhận")
        button_yes.grid(row=1, column=0, sticky="w", padx=10)
        button_yes.config(command=partial(self.destroy_all_by_cancel))
        button_no = ButtonType.primary(self.view_cancel_top_window, "Không")
        button_no.grid(row=1, column=0, sticky="e", padx=10)
        button_no.config(command=self.view_cancel_top_window.destroy)
        
    def show_column_title(self):
        column = 0
        for j in self.coloumn_title:
            if j == 'Mã bán hàng' or j == 'Ngày bán' or j == 'Mã hàng':
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
        self.sub_frame_bottom_top.columnconfigure(4, weight=1)
        self.sub_frame_bottom_top.columnconfigure(5, weight=1)
        
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
        head_label = LabelType.h1(self.sub_frame_bottom_top, "Thêm bán hàng") # Label trong head_frame
        head_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        button_refresh = ButtonType.brown(self.sub_frame_bottom_top, "Làm mới dữ liệu")
        button_refresh.grid(row=0, column=2, padx=5, pady=5, columnspan=2)
        button_refresh.config(command=partial(self.refresh_ban_hang_list))
        button_export = ButtonType.success(self.sub_frame_bottom_top, "Xuất hóa đơn")
        button_export.grid(row=0, column=4, padx=5, pady=5, columnspan=2)
        button_export.config(command=partial(self.export_invoice))
        total_ban_hang_label = LabelType.normal_blue_white(self.sub_frame_bottom_top, text="Tổng bán hàng:")
        total_ban_hang_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        total_ban_hang_value = EntryType.view(self.sub_frame_bottom_top, text_var=self.total_ban_hang)
        total_ban_hang_value.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        total_so_luong_label = LabelType.normal_blue_white(self.sub_frame_bottom_top, text="Tổng số lượng:")
        total_so_luong_label.grid(row=1, column=2, sticky='e', padx=5, pady=5)
        total_so_luong_value = EntryType.view(self.sub_frame_bottom_top, text_var=self.total_so_luong)
        total_so_luong_value.grid(row=1, column=3, sticky='w', padx=5, pady=5)
        total_thanh_tien_label = LabelType.normal_blue_white(self.sub_frame_bottom_top, text="Tổng thành tiền:")
        total_thanh_tien_label.grid(row=1, column=4, sticky='e', padx=5, pady=5)
        total_thanh_tien_value = EntryType.view(self.sub_frame_bottom_top, text_var=self.total_thanh_tien)
        total_thanh_tien_value.grid(row=1, column=5, sticky='w', padx=5, pady=5)
        
        # ---- sub_frame_bottom_bottom ----
        button_add = ButtonType.success(self.sub_frame_bottom_bottom, "Lưu toàn bộ bán hàng")
        button_add.config(command=partial(self.save_all))
        button_add.grid(row=0, column=0, padx=5, pady=5)
        button_cancel = ButtonType.danger(self.sub_frame_bottom_bottom, "Hủy")
        button_cancel.config(command=partial(self.view_cancel))
        button_cancel.grid(row=0, column=1, padx=5, pady=5)
        
        # Tạo ô bán văn bản (Entry) cho tìm kiếm hàng hóa
        search_input_box = EntryType.blue(self.sub_frame_top, text_var=self.search_mat_hang_var)
        search_input_box.grid(row=0, column=0, sticky='se', pady=5)
        search_input_box.bind("<KeyRelease>", self.on_search_mat_hang) # Liên kết sự kiện bán văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.sub_frame_top, "Tìm kiếm mặt hàng")
        search_button.config(command=partial(self.on_search_mat_hang_button_click))
        search_button.grid(row=0, column=1, sticky='sw', padx=5)
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_mat_hang_box = Listbox(self.sub_frame_top, font=FontType.normal(), height=10, width=50)
        self.suggestion_mat_hang_box.grid(row=1, column=0, columnspan=2)
        self.suggestion_mat_hang_box.bind("<<ListboxSelect>>", self.on_suggestion_mat_hang_select)
        
        # Tạo ô bán văn bản (Entry) cho tìm kiếm khach_hang
        search_input_box = EntryType.blue(self.sub_frame_top, text_var=self.search_khach_hang_var)
        search_input_box.grid(row=0, column=2, sticky='se', pady=5)
        search_input_box.bind("<KeyRelease>", self.on_search_khach_hang) # Liên kết sự kiện bán văn bản với hàm xử lý
        # Tạo nút tìm kiếm
        search_button = ButtonType.primary(self.sub_frame_top, "Tìm kiếm khách hàng")
        search_button.config(command=partial(self.on_search_khach_hang_button_click))
        search_button.grid(row=0, column=3, sticky='sw', padx=5)
        # Tạo Listbox cho gợi ý từ khóa
        self.suggestion_khach_hang_box = Listbox(self.sub_frame_top, font=FontType.normal(), height=10, width=50)
        self.suggestion_khach_hang_box.grid(row=1, column=2, columnspan=2)
        self.suggestion_khach_hang_box.bind("<<ListboxSelect>>", self.on_suggestion_khach_hang_select)
        
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
        
    def register_fonts(self):
        # Đăng ký phông chữ Arial
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
          