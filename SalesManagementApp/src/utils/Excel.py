import pandas as pd
import logging
from src.entity.MatHangEntity import MatHang
from src.entity.NhapHangEntity import NhapHang
from src.entity.BanHangEntity import BanHang
from src.entity.ChiPhiEntity import ChiPhi
from src.entity.KhachHangEntity import KhachHang
from src.entity.NccEntity import NCC
from tkinter import filedialog, messagebox
from datetime import datetime

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
        from src.service.MatHangService import MatHangService
        mat_hang_service = MatHangService()
        df = pd.read_excel(path, engine='openpyxl')
        df_filled = df.fillna({
            'ten_hang': 'Không rõ',
            'don_vi': '',
            'so_luong': 0,
            'gia_le': 0,
            'gia_si': 0,
            'ngay_tao': datetime.now().strftime('%Y-%m-%d'),
            'is_active': 1
        })
        for index, row in df_filled.iterrows():
            mat_hang = MatHang(
                ten_hang=row.get('ten_hang'),
                don_vi=row.get('don_vi'),
                so_luong=row.get('so_luong'),
                gia_le=row.get('gia_le'),
                gia_si=row.get('gia_si'),
                ngay_tao=row.get('ngay_tao'),
                is_active=row.get('is_active')
            )
            mat_hang_service.create(mat_hang)
        messagebox.showinfo("Import dữ liệu thành công", f"Đã import dữ liệu từ file excel: {path}")
        return True
      
    def import_khach_hang(self, path: str) -> bool:
        from src.service.KhachHangService import KhachHangService
        khach_hang_service = KhachHangService()
        df = pd.read_excel(path, engine='openpyxl')
        df_filled = df.fillna({
            'ten_khach_hang': 'Không rõ',
            'dia_chi': '',
            'so_dien_thoai': '',
            'email': '',
            'ghi_chu': '',
            'ngay_tao': datetime.now().strftime('%Y-%m-%d'),
            'is_active': 1
        })
        for index, row in df_filled.iterrows():
            khach_hang = KhachHang(
                ten_khach_hang=row.get('ten_khach_hang'),
                dien_thoai=row.get('so_dien_thoai'),
                email=row.get('email'),
                dia_chi=row.get('dia_chi'),
                ghi_chu=row.get('ghi_chu'),
                ngay_tao=row.get('ngay_tao'),
                is_active=row.get('is_active')
            )
            khach_hang_service.create(khach_hang)
        messagebox.showinfo("Import dữ liệu thành công", f"Đã import dữ liệu từ file excel: {path}")
        return True
      
    def import_ncc(self, path: str) -> bool:
        from src.service.NccService import NCCService
        ncc_service = NCCService()
        df = pd.read_excel(path, engine='openpyxl')
        df_filled = df.fillna({
            'ten_ncc': 'Không rõ',
            'dia_chi': '',
            'so_dien_thoai': '',
            'email': '',
            'ghi_chu': '',
            'ngay_tao': datetime.now().strftime('%Y-%m-%d'),
            'is_active': 1
        })
        for index, row in df_filled.iterrows():
            ncc = NCC(
                ten_ncc=row.get('ten_ncc'),
                dien_thoai=row.get('so_dien_thoai'),
                email=row.get('email'),
                dia_chi=row.get('dia_chi'),
                ghi_chu=row.get('ghi_chu'),
                ngay_tao=row.get('ngay_tao'),
                is_active=row.get('is_active')
            )
            ncc_service.create(ncc)
        messagebox.showinfo("Import dữ liệu thành công", f"Đã import dữ liệu từ file excel: {path}")
        return True
      
    def import_chi_phi(self, path: str) -> bool:
        from src.service.ChiPhiService import ChiPhiService
        chi_phi_service = ChiPhiService()
        df = pd.read_excel(path, engine='openpyxl')
        df_filled = df.fillna({
            'ten_chi_phi': 'Không rõ',
            'gia_chi_phi': 0,
            'ghi_chu': '',
            'ngay_tao': datetime.now().strftime('%Y-%m-%d')
        })
        for index, row in df_filled.iterrows():
            chi_phi = ChiPhi(
                ten_chi_phi=row.get('ten_chi_phi'),
                gia_chi_phi=row.get('gia_chi_phi'),
                ghi_chu=row.get('ghi_chu'),
                ngay_tao=row.get('ngay_tao')
            )
            chi_phi_service.create(chi_phi)
        messagebox.showinfo("Import dữ liệu thành công", f"Đã import dữ liệu từ file excel: {path}")
        return True
        
    def import_nhap_hang(self, path: str) -> bool:
        from src.service.NhapHangService import NhapHangService
        nhap_hang_service = NhapHangService()
        df = pd.read_excel(path, engine='openpyxl')
        df_filled = df.fillna({
            'id_mat_hang': '',
            'ten_hang': 'Không rõ',
            'don_vi': '',
            'nha_cung_cap': '',
            'so_luong': 0,
            'gia_nhap': 0,
            'thanh_tien': 0,
            'ghi_chu': '',
            'ngay_nhap': datetime.now().strftime('%Y-%m-%d')
        })
        for index, row in df_filled.iterrows():
            nhap_hang = NhapHang(
                id_mat_hang=row.get('id_mat_hang'),
                ten_hang=row.get('ten_hang'),
                don_vi=row.get('don_vi'),
                nha_cung_cap=row.get('nha_cung_cap'),
                so_luong=row.get('so_luong'),
                gia_nhap=row.get('gia_nhap'),
                thanh_tien=row.get('thanh_tien'),
                ghi_chu=row.get('ghi_chu'),
                ngay_nhap=row.get('ngay_nhap')
            )
            nhap_hang_service.create(nhap_hang)
        messagebox.showinfo("Import dữ liệu thành công", f"Đã import dữ liệu từ file excel: {path}")
        return True
      
    def import_ban_hang(self, path: str) -> bool:
        from src.service.BanHangService import BanHangService
        ban_hang_service = BanHangService()
        df = pd.read_excel(path, engine='openpyxl')
        df_filled = df.fillna({
            'id_mat_hang': '',
            'ten_hang': 'Không rõ',
            'don_vi': '',
            'khach_hang': '',
            'so_luong': 0,
            'gia_ban': 0,
            'thanh_tien': 0,
            'ghi_chu': '',
            'ngay_ban': datetime.now().strftime('%Y-%m-%d')
        })
        for index, row in df_filled.iterrows():
            ban_hang = BanHang(
                id_mat_hang=row.get('id_mat_hang'),
                ten_hang=row.get('ten_hang'),
                don_vi=row.get('don_vi'),
                khach_hang=row.get('khach_hang'),
                so_luong=row.get('so_luong'),
                gia_ban=row.get('gia_ban'),
                thanh_tien=row.get('thanh_tien'),
                ghi_chu=row.get('ghi_chu'),
                ngay_ban=row.get('ngay_ban')
            )
            ban_hang_service.create(ban_hang)
        messagebox.showinfo("Import dữ liệu thành công", f"Đã import dữ liệu từ file excel: {path}")
        return True
      
    def select_folder_export(self):
        # Mở hộp thoại chọn thư mục
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            messagebox.showinfo("Thư mục đã chọn", f"Thư mục đã chọn: {folder_selected}")
            return folder_selected
        else:
            messagebox.showwarning("Chưa chọn thư mục", "Bạn chưa chọn thư mục nào.")
            return None
        
    def select_file_import(self):
        # Mở hộp thoại chọn thư mục
        file_selected = filedialog.askopenfilename()
        if file_selected and (file_selected.endswith('.xlsx') or file_selected.endswith('.xls')):
            return file_selected
        else:
            messagebox.showwarning("Lỗi chọn file", "Bạn cần chọn file excel (.xlsx hoặc .xls)")
            return None