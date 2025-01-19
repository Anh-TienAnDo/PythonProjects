from datetime import datetime
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
from contants import NCC_ID_PREFIX, NCC_ID_LENGTH, NCC_TABLE


class NCC:
    def __init__(self, id=None, ten_ncc=None, dien_thoai=None, email=None, dia_chi=None, ghi_chu=None, ngay_tao=None, is_active=None):
        self.id = id if id is not None else GenerationId.generate_id(
            NCC_ID_LENGTH, NCC_ID_PREFIX)
        self.ten_ncc = TextNormalization.remove_special_characters_and_Upper(str(ten_ncc)) if ten_ncc is not None else ""
        self.dien_thoai = TextNormalization.remove_special_characters(str(dien_thoai)) if dien_thoai is not None else ""
        self.email = TextNormalization.remove_special_characters(str(email)) if email is not None else ""
        self.dia_chi = TextNormalization.remove_special_characters(str(dia_chi)) if dia_chi is not None else ""
        self.ghi_chu = TextNormalization.remove_special_characters(str(ghi_chu)) if ghi_chu is not None else ""
        self.ngay_tao = ngay_tao if ngay_tao is not None else datetime.now().strftime("%Y-%m-%d")
        self.is_active = is_active if is_active is not None else 1

    def __repr__(self):
        return f"{NCC_TABLE}(id={self.id}, ten_ncc={self.ten_ncc}, dien_thoai={self.dien_thoai}, email={self.email}, dia_chi={self.dia_chi}, ghi_chu={self.ghi_chu}, ngay_tao={self.ngay_tao}, is_active={self.is_active})"

    def to_tuple(self):
        return (self.id, self.ten_ncc, self.dien_thoai, self.email, self.dia_chi, self.ghi_chu, self.ngay_tao, self.is_active)
    
    def to_dict(self):
        return {
            "id": self.id,
            "ten_ncc": self.ten_ncc,
            "dien_thoai": self.dien_thoai,
            "email": self.email,
            "dia_chi": self.dia_chi,
            "ghi_chu": self.ghi_chu,
            "ngay_tao": self.ngay_tao,
            "is_active": self.is_active
        }
        
    def to_list(self):
        return [self.id, self.ten_ncc, self.dien_thoai, self.email, self.dia_chi, self.ghi_chu, self.ngay_tao, self.is_active]
