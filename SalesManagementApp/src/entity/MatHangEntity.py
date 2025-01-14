from datetime import datetime
from src.utils.GenerationId import GenerationId
from contants import MAT_HANG_ID_PREFIX, MAT_HANG_ID_LENGTH, MAT_HANG_TABLE

class MatHang:
    def __init__(
        self, id, ten_hang, don_vi, so_luong, gia_le, gia_si, ngay_tao, is_active
    ):
        self.id = id if id is not None else GenerationId.generate_id(MAT_HANG_ID_LENGTH, MAT_HANG_ID_PREFIX)
        self.ten_hang = ten_hang
        self.don_vi = don_vi
        self.so_luong = so_luong
        self.gia_le = gia_le
        self.gia_si = gia_si
        self.ngay_tao = ngay_tao if ngay_tao is not None else datetime.now().strftime("%Y-%m-%d")
        self.is_active = is_active if is_active is not None else 1

    def __repr__(self):
        return f"{MAT_HANG_TABLE}(id={self.id}, ten_hang={self.ten_hang}, don_vi={self.don_vi}, so_luong={self.so_luong}, gia_le={self.gia_le}, gia_si={self.gia_si}, ngay_tao={self.ngay_tao}, is_active={self.is_active})"
    
    def to_tuple(self):
        return (self.id, self.ten_hang, self.don_vi, self.so_luong, self.gia_le, self.gia_si, self.ngay_tao, self.is_active)

