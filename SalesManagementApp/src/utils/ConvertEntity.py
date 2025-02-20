from concurrent.futures import ThreadPoolExecutor
from abc import ABC, abstractmethod

from src.entity.ChiPhiEntity import ChiPhi
from src.entity.KhachHangEntity import KhachHang
from src.entity.NccEntity import NCC
from src.entity.NhapHangEntity import NhapHang
from src.entity.BanHangEntity import BanHang
from src.entity.MatHangEntity import MatHang

class ConvertEntity(ABC):
    @abstractmethod
    def convert_to_entity(self, data):
        pass
    
    @abstractmethod
    def convert_to_entity_list(self, data):
        pass
    
class ConvertBanHang(ConvertEntity):
    def __init__(self):
        pass
    
    def convert_to_entity_list(self, data):
        with ThreadPoolExecutor(max_workers=5) as executor:
            ban_hang_list = list(executor.submit(self.convert_to_entity, row).result() for row in data)
        return ban_hang_list
    
    def convert_to_entity(self, data):
        return BanHang(*data)       
    
class ConvertMatHang(ConvertEntity):
    def __init__(self):
        pass
    
    def convert_to_entity_list(self, data):
        with ThreadPoolExecutor(max_workers=5) as executor:
            mat_hang_list = list(executor.submit(self.convert_to_entity, row).result() for row in data)
        return mat_hang_list
    
    def convert_to_entity(self, data):
        return MatHang(*data)
    
class ConvertNCC(ConvertEntity):
    def __init__(self):
        pass
    
    def convert_to_entity_list(self, data):
        with ThreadPoolExecutor(max_workers=5) as executor:
            ncc_list = list(executor.submit(self.convert_to_entity, row).result() for row in data)
        return ncc_list
    
    def convert_to_entity(self, data):
        return NCC(*data)
    
class ConvertKhachHang(ConvertEntity):
    def __init__(self):
        pass
    
    def convert_to_entity_list(self, data):
        with ThreadPoolExecutor(max_workers=5) as executor:
            khach_hang_list = list(executor.submit(self.convert_to_entity, row).result() for row in data)
        return khach_hang_list
    
    def convert_to_entity(self, data):
        return KhachHang(*data)
    
class ConvertChiPhi(ConvertEntity):
    def __init__(self):
        pass
    
    def convert_to_entity_list(self, data):
        with ThreadPoolExecutor(max_workers=5) as executor:
            chi_phi_list = list(executor.submit(self.convert_to_entity, row).result() for row in data)
        return chi_phi_list
    
    def convert_to_entity(self, data):
        return ChiPhi(*data)
    
class ConvertNhapHang(ConvertEntity):
    def __init__(self):
        pass
    
    def convert_to_entity_list(self, data):
        with ThreadPoolExecutor(max_workers=5) as executor:
            nhap_hang_list = list(executor.submit(self.convert_to_entity, row).result() for row in data)
        return nhap_hang_list
    
    def convert_to_entity(self, data):
        return NhapHang(*data)
    
