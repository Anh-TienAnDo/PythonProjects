from datetime import datetime
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
from contants import CHI_PHI_ID_PREFIX, CHI_PHI_ID_LENGTH, CHI_PHI_TABLE


class ChiPhi:
    def __init__(self, id=None, ten_chi_phi=None, gia_chi_phi=None, ghi_chu=None, ngay_tao=None):
        self.id = id if id is not None else GenerationId.generate_id(
            CHI_PHI_ID_LENGTH, CHI_PHI_ID_PREFIX)
        self.ten_chi_phi = TextNormalization.remove_special_characters_and_Upper(str(ten_chi_phi)) if ten_chi_phi is not None else ""
        self.gia_chi_phi = int(gia_chi_phi) if gia_chi_phi is not None and str(gia_chi_phi).isdigit() else 0
        self.ghi_chu = TextNormalization.remove_special_characters(str(ghi_chu)) if ghi_chu is not None else ""
        self.ngay_tao = ngay_tao if ngay_tao is not None else datetime.now().strftime("%Y-%m-%d")

    def __repr__(self):
        return f"{CHI_PHI_TABLE}(id={self.id}, ten_chi_phi={self.ten_chi_phi}, gia_chi_phi={self.gia_chi_phi}, ghi_chu={self.ghi_chu}, ngay_tao={self.ngay_tao})"

    def to_tuple(self):
        return (self.id, self.ten_chi_phi, self.gia_chi_phi, self.ghi_chu, self.ngay_tao)
    
    def to_dict(self):
        return {
            "id": self.id,
            "ten_chi_phi": self.ten_chi_phi,
            "gia_chi_phi": self.gia_chi_phi,
            "ghi_chu": self.ghi_chu,
            "ngay_tao": self.ngay_tao
        }
        
    def to_list(self):
        return [self.id, self.ten_chi_phi, self.gia_chi_phi, self.ghi_chu, self.ngay_tao]
