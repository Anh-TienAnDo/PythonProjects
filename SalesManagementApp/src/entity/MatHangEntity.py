from datetime import datetime
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
from contants import MAT_HANG_ID_PREFIX, MAT_HANG_ID_LENGTH, MAT_HANG_TABLE


class MatHang:
    def __init__(self, id=None, ten_hang=None, don_vi=None, so_luong=None, gia_le=None, gia_si=None, ngay_tao=None, is_active=None):
        self.id = id if id is not None else GenerationId.generate_id(
            MAT_HANG_ID_LENGTH, MAT_HANG_ID_PREFIX)
        self.ten_hang = TextNormalization.remove_special_characters(str(ten_hang)) if ten_hang is not None else ""
        self.don_vi = TextNormalization.remove_special_characters(str(don_vi)) if don_vi is not None else ""
        self.so_luong = int(so_luong) if so_luong is not None else 0
        self.gia_le = int(gia_le) if gia_le is not None else 0
        self.gia_si = int(gia_si) if gia_si is not None else 0
        self.ngay_tao = ngay_tao if ngay_tao is not None else datetime.now().strftime("%Y-%m-%d")
        self.is_active = is_active if is_active is not None else 1

    def __repr__(self):
        return f"{MAT_HANG_TABLE}(id={self.id}, ten_hang={self.ten_hang}, don_vi={self.don_vi}, so_luong={self.so_luong}, gia_le={self.gia_le}, gia_si={self.gia_si}, ngay_tao={self.ngay_tao}, is_active={self.is_active})"

    def to_tuple(self):
        return (self.id, self.ten_hang, self.don_vi, self.so_luong, self.gia_le, self.gia_si, self.ngay_tao, self.is_active)
    
    def to_dict(self):
        return {
            "id": self.id,
            "ten_hang": self.ten_hang,
            "don_vi": self.don_vi,
            "so_luong": self.so_luong,
            "gia_le": self.gia_le,
            "gia_si": self.gia_si,
            "ngay_tao": self.ngay_tao,
            "is_active": self.is_active
        }
        
    def to_list(self):
        return [self.id, self.ten_hang, self.don_vi, self.so_luong, self.gia_le, self.gia_si, self.ngay_tao, self.is_active]
