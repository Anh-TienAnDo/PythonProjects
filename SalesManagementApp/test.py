import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class NhapHangAddController:
    def __init__(self, frame: tk.Frame):
        self.frame = frame
        # Thêm nút để chọn thư mục lưu trữ
        select_folder_button = tk.Button(self.frame, text="Xuất hóa đơn", command=self.select_folder)
        select_folder_button.pack(pady=20)
        # Dữ liệu hóa đơn mẫu
        self.invoice_data = {
            "Mã hóa đơn": "HD001",
            "Ngày": datetime.now().strftime("%d/%m/%Y"),
            "Khách hàng": "Nguyễn Văn A",
            "items": [
                {"name": "Sản phẩm A", "quantity": 2, "price": "100.000"},
                {"name": "Sản phẩm B", "quantity": 1, "price": "200.000"},
                {"name": "Sản phẩm C", "quantity": 3, "price": "150.000"},
            ],
            "total": "650.000"
        }
        
        # Đăng ký phông chữ Arial
        self.register_fonts()
        # # Thêm nút để tạo và in hóa đơn
        # self.print_button = tk.Button(self.frame, text="In hóa đơn", command=self.create_and_print_invoice)
        # self.print_button.pack(pady=20)

    def select_folder(self):
        # Mở hộp thoại chọn thư mục
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            messagebox.showinfo("Thư mục đã chọn", f"Thư mục đã chọn: {folder_selected}")
            self.selected_folder = folder_selected
            # Tạo tài liệu PDF
            pdf_filename = f"{self.selected_folder}/invoice_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
            self.create_invoice_pdf(pdf_filename)
            messagebox.showinfo(f"Đã xuất hóa đơn tại: {pdf_filename}")
        else:
            messagebox.showwarning("Chưa chọn thư mục", "Bạn chưa chọn thư mục nào.")

    def create_invoice_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Tiêu đề hóa đơn
        c.setFont("Arial", 20)
        c.drawString(200, height - 50, "HÓA ĐƠN BÁN HÀNG")

        # Thông tin hóa đơn
        c.setFont("Arial", 12)
        y = height - 100
        for key, value in self.invoice_data.items():
            if key != "items":
                c.drawString(50, y, f"{key}: {value}")
                y -= 20

        # Thông tin sản phẩm
        c.drawString(50, y, "Sản phẩm:")
        y -= 20
        for item in self.invoice_data['items']:
            c.drawString(70, y, f"{item['name']} - Số lượng: {item['quantity']} - Giá: {item['price']}")
            y -= 20

        # Tổng cộng
        c.drawString(50, y, f"Tổng cộng: {self.invoice_data['total']}")

        c.save()

    def register_fonts(self):
        # Đăng ký phông chữ Arial
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = NhapHangAddController(root)
    root.mainloop()