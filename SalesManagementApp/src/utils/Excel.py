import pandas as pd
import logging
from src.entity.MatHangEntity import MatHang
from src.entity.NhapHangEntity import NhapHang
from src.entity.BanHangEntity import BanHang
from src.entity.ChiPhiEntity import ChiPhi
from src.entity.KhachHangEntity import KhachHang
from src.entity.NccEntity import NCC
from tkinter import filedialog, messagebox

class Excel:
    def __init__(self):
        pass

    def export_data(self, path: str, data: list[dict]) -> bool:
        try:
            data_dict = {}
            for d in data:
                for key in d.keys():
                    if key in data_dict:
                        data_dict[key].append(d[key])
                    else:
                        data_dict[key] = [d[key]]
            data_frame = pd.DataFrame(data_dict)
            data_frame.to_excel(path, index=False, engine='openpyxl')
            messagebox.showinfo("Xuất file thành công", f"Đã xuất file excel tại đường dẫn: {path}")
            return True
        except Exception as e:
            logging.error(f'Error when exporting data to excel: {e}')
            messagebox.showerror("Xuất file thất bại", f"Đã có lỗi xảy ra khi xuất file excel: {e}")
            return False

    def import_mat_hang(self, path: str) -> bool:
        pass
      
    def import_khach_hang(self, path: str) -> bool:
        pass
      
    def import_ncc(self, path: str) -> bool:
        pass
      
    def import_chi_phi(self, path: str) -> bool:
        pass
      
    def import_nhap_hang(self, path: str) -> bool:
        pass
      
    def import_ban_hang(self, path: str) -> bool:
        pass
      
    def select_folder(self):
        # Mở hộp thoại chọn thư mục
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            messagebox.showinfo("Thư mục đã chọn", f"Thư mục đã chọn: {folder_selected}")
            return folder_selected
        else:
            messagebox.showwarning("Chưa chọn thư mục", "Bạn chưa chọn thư mục nào.")
            return None