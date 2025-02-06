from datetime import datetime
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
from contants import KHACH_HANG_ID_PREFIX, KHACH_HANG_ID_LENGTH, KHACH_HANG_TABLE


class KhachHang:
    def __init__(self, id=None, ten_khach_hang=None, dien_thoai=None, email=None, dia_chi=None, ghi_chu=None, ngay_tao=None, is_active=None):
        self.id = id if id is not None and KHACH_HANG_ID_PREFIX in id else GenerationId.generate_id(
            KHACH_HANG_ID_LENGTH, KHACH_HANG_ID_PREFIX)
        self.ten_khach_hang = TextNormalization.remove_special_characters_and_Upper(str(ten_khach_hang)) if ten_khach_hang is not None else ""
        self.dien_thoai = TextNormalization.remove_special_characters(str(dien_thoai)) if dien_thoai is not None else ""
        self.email = str(email).strip() if email is not None else ""
        self.dia_chi = str(dia_chi).strip() if dia_chi is not None else ""
        self.ghi_chu = str(ghi_chu).strip() if ghi_chu is not None else ""
        self.ngay_tao = ngay_tao if ngay_tao is not None else datetime.now().strftime("%Y-%m-%d")
        self.is_active = is_active if is_active is not None else 1

    def __repr__(self):
        return f"{KHACH_HANG_TABLE}(id={self.id}, ten_khach_hang={self.ten_khach_hang}, dien_thoai={self.dien_thoai}, email={self.email}, dia_chi={self.dia_chi}, ghi_chu={self.ghi_chu}, ngay_tao={self.ngay_tao}, is_active={self.is_active})"

    def to_tuple(self):
        return (self.id, self.ten_khach_hang, self.dien_thoai, self.email, self.dia_chi, self.ghi_chu, self.ngay_tao, self.is_active)
    
    def to_dict(self):
        return {
            "id": self.id,
            "ten_khach_hang": self.ten_khach_hang,
            "dien_thoai": self.dien_thoai,
            "email": self.email,
            "dia_chi": self.dia_chi,
            "ghi_chu": self.ghi_chu,
            "ngay_tao": self.ngay_tao,
            "is_active": self.is_active
        }
        
    def to_list(self):
        return [self.id, self.ten_khach_hang, self.dien_thoai, self.email, self.dia_chi, self.ghi_chu, self.ngay_tao, self.is_active]
