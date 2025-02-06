from datetime import datetime
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
from contants import NHAP_HANG_ID_PREFIX, NHAP_HANG_ID_LENGTH, NHAP_HANG_TABLE


class NhapHang:
    def __init__(self, id=None, id_mat_hang=None, ten_hang=None, don_vi=None, so_luong=None, gia_nhap=None, nha_cung_cap=None, thanh_tien=None, ghi_chu=None, ngay_nhap=None):
        self.id = id if id is not None and NHAP_HANG_ID_PREFIX in id else GenerationId.generate_id(NHAP_HANG_ID_LENGTH, NHAP_HANG_ID_PREFIX)
        self.id_mat_hang = str(id_mat_hang)
        self.ten_hang = str(ten_hang)
        self.don_vi = TextNormalization.remove_special_characters(str(don_vi)) if don_vi is not None else ""
        self.so_luong = int(so_luong) if so_luong is not None and str(so_luong).strip().isdigit() else 0
        self.gia_nhap = int(gia_nhap) if gia_nhap is not None and str(gia_nhap).strip().isdigit() else 0
        self.nha_cung_cap = str(nha_cung_cap).strip() if nha_cung_cap is not None else ""
        self.thanh_tien = int(thanh_tien) if thanh_tien is not None and str(thanh_tien).strip().isdigit() else 0
        self.ghi_chu = str(ghi_chu).strip() if ghi_chu is not None else ""
        self.ngay_nhap = ngay_nhap if ngay_nhap is not None else datetime.now().strftime("%Y-%m-%d")
        
    def __repr__(self):
        return f"{NHAP_HANG_TABLE}(id={self.id}, id_mat_hang={self.id_mat_hang}, ten_hang={self.ten_hang}, don_vi={self.don_vi}, so_luong={self.so_luong}, gia_nhap={self.gia_nhap}, nha_cung_cap={self.nha_cung_cap}, thanh_tien={self.thanh_tien}, ghi_chu={self.ghi_chu}, ngay_nhap={self.ngay_nhap})"
      
    def to_tuple(self):
        return (self.id, self.id_mat_hang, self.ten_hang, self.don_vi, self.so_luong, self.gia_nhap, self.nha_cung_cap, self.thanh_tien, self.ghi_chu, self.ngay_nhap)
      
    def to_dict(self):
        return {
            "id": self.id,
            "id_mat_hang": self.id_mat_hang,
            "ten_hang": self.ten_hang,
            "don_vi": self.don_vi,
            "so_luong": self.so_luong,
            "gia_nhap": self.gia_nhap,
            "nha_cung_cap": self.nha_cung_cap,
            "thanh_tien": self.thanh_tien,
            "ghi_chu": self.ghi_chu,
            "ngay_nhap": self.ngay_nhap
        }
      
    def to_list(self):
        return [self.id, self.id_mat_hang, self.ten_hang, self.don_vi, self.so_luong, self.gia_nhap, self.nha_cung_cap, self.thanh_tien, self.ghi_chu, self.ngay_nhap]
    
