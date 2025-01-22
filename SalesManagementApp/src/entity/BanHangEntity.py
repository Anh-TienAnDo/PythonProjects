from datetime import datetime
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
from contants import BAN_HANG_ID_PREFIX, BAN_HANG_ID_LENGTH, BAN_HANG_TABLE


class BanHang:
    def __init__(self, id=None, id_mat_hang=None, ten_hang=None, don_vi=None, so_luong=None, gia_ban=None, khach_hang=None, thanh_tien=None, ghi_chu=None, ngay_ban=None):
        self.id = id if id is not None else GenerationId.generate_id(BAN_HANG_ID_LENGTH, BAN_HANG_ID_PREFIX)
        self.id_mat_hang = str(id_mat_hang)
        self.ten_hang = str(ten_hang)
        self.don_vi = TextNormalization.remove_special_characters(str(don_vi)) if don_vi is not None else ""
        self.so_luong = int(so_luong) if so_luong is not None and str(so_luong).isdigit() else 0
        self.gia_ban = int(gia_ban) if gia_ban is not None and str(gia_ban).isdigit() else 0
        self.khach_hang = str(khach_hang).strip() if khach_hang is not None else ""
        self.thanh_tien = int(thanh_tien) if thanh_tien is not None and str(thanh_tien).isdigit() else 0
        self.ghi_chu = str(ghi_chu).strip() if ghi_chu is not None else ""
        self.ngay_ban = ngay_ban if ngay_ban is not None else datetime.now().strftime("%Y-%m-%d")
        
    def __repr__(self):
        return f"{BAN_HANG_TABLE}(id={self.id}, id_mat_hang={self.id_mat_hang}, ten_hang={self.ten_hang}, don_vi={self.don_vi}, so_luong={self.so_luong}, gia_ban={self.gia_ban}, khach_hang={self.khach_hang}, thanh_tien={self.thanh_tien}, ghi_chu={self.ghi_chu}, ngay_ban={self.ngay_ban})"
      
    def to_tuple(self):
        return (self.id, self.id_mat_hang, self.ten_hang, self.don_vi, self.so_luong, self.gia_ban, self.khach_hang, self.thanh_tien, self.ghi_chu, self.ngay_ban)
      
    def to_dict(self):
        return {
            "id": self.id,
            "id_mat_hang": self.id_mat_hang,
            "ten_hang": self.ten_hang,
            "don_vi": self.don_vi,
            "so_luong": self.so_luong,
            "gia_ban": self.gia_ban,
            "khach_hang": self.khach_hang,
            "thanh_tien": self.thanh_tien,
            "ghi_chu": self.ghi_chu,
            "ngay_ban": self.ngay_ban
        }
      
    def to_list(self):
        return [self.id, self.id_mat_hang, self.ten_hang, self.don_vi, self.so_luong, self.gia_ban, self.khach_hang, self.thanh_tien, self.ghi_chu, self.ngay_ban]
    
