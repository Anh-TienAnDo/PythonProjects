from src.entity.NhapHangEntity import NhapHang
from src.entity.ChiPhiEntity import ChiPhi
from src.repository.NhapHangRepo import NhapHangRepo
from src.service.MatHangService import MatHangService
from src.service.ChiPhiService import ChiPhiService
from src.config.search_whoosh import SearchWhooshMatHang, SearchWhooshNCC
from src.utils.GenerationId import GenerationId
import logging
from contants import NHAP_HANG_SORT_OPTIONS, NHAP_HANG_ID_PREFIX, NHAP_HANG_ID_LENGTH
from datetime import datetime

class NhapHangService:
    def __init__(self):
        logging.info('---NhapHangService initializing---')
        self.nhap_hang_repo = NhapHangRepo()
        self.mat_hang_search = SearchWhooshMatHang()
        self.ncc_search = SearchWhooshNCC()
        self.mat_hang_service = MatHangService()
        self.chi_phi_service = ChiPhiService()

    def get_all(self, sort: str, day: str, month: str, year: str) -> list[NhapHang]:
        sort = sort.strip()
        if sort not in self.get_nhap_hang_sort_keys() or sort == '' or sort is None:
            sort = 'Tên A-Z'
        sort_by = self.get_nhap_hang_sort_by_key(sort)

        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        if month is None or month.strip() == '':
            month = str(now.month)
        if year is None or year.strip() == '':
            year = str(now.year)
        if len(month) == 1:
            month = f'0{month}'
        if day is None or day.strip() == '':
            where = f"strftime('%m-%Y', ngay_nhap) = '{month}-{year}'"
        else:
            if len(day) == 1:
                day = f'0{day}'
            where = f"strftime('%d-%m-%Y', ngay_nhap) = '{day}-{month}-{year}'"
        return self.nhap_hang_repo.get_all(sort_by, where)
        
    def get_by_id(self, nhap_hang_id) -> NhapHang:
        return self.nhap_hang_repo.get_by_id(nhap_hang_id)

    def create(self, nhap_hang: NhapHang) -> bool:
        while self.nhap_hang_repo.check_exist_id(nhap_hang.id):
            nhap_hang.id = GenerationId.generate_id(NHAP_HANG_ID_LENGTH, NHAP_HANG_ID_PREFIX)
        if not self.nhap_hang_repo.create(nhap_hang):
            return False
        # update số lượng mặt hàng, create chi phí
        chi_phi = ChiPhi()
        chi_phi.ten_chi_phi = nhap_hang.id
        chi_phi.gia_chi_phi = nhap_hang.thanh_tien
        chi_phi.ghi_chu = "Nhập hàng"
        if not self.chi_phi_service.create(chi_phi):
            return False
        mat_hang = self.mat_hang_service.get_by_id(nhap_hang.id_mat_hang)
        if mat_hang is None:
            return False
        mat_hang.so_luong += nhap_hang.so_luong
        if not self.mat_hang_service.update(mat_hang.id, mat_hang):
            return False
        print('Create nhap hang success')
        print(nhap_hang.to_dict())
        print(chi_phi.to_dict())
        print(mat_hang.to_dict())
        return True

    def update(self, nhap_hang_id, nhap_hang: NhapHang, so_luong_nhap_old: int) -> bool:
        if not self.nhap_hang_repo.check_exist_id(nhap_hang_id):
            return False
        if not self.nhap_hang_repo.update(nhap_hang_id, nhap_hang):
            return False
        # update số lượng mặt hàng: có mặt hàng cũ và số lượng mới, update giá chi phí
        chi_phi = self.chi_phi_service.get_by_ten_chi_phi(nhap_hang_id)
        chi_phi.gia_chi_phi = nhap_hang.thanh_tien
        if not self.chi_phi_service.update(chi_phi.id, chi_phi):
            return False
        mat_hang = self.mat_hang_service.get_by_id(nhap_hang.id_mat_hang)
        if mat_hang is None:
            return False
        mat_hang.so_luong = mat_hang.so_luong - so_luong_nhap_old + nhap_hang.so_luong
        if not self.mat_hang_service.update(mat_hang.id, mat_hang):
            return False
        print('Update nhap hang success')
        print(nhap_hang.to_dict())
        print(chi_phi.to_dict())
        print(mat_hang.to_dict())
        return True
      
    def delete(self, nhap_hang_id) -> bool: #--------------------------------------------------------
        if not self.nhap_hang_repo.check_exist_id(nhap_hang_id):
            return False
        # update số lượng mặt hàng: xóa số lượng của nhập hàng, delete chi phí
        nhap_hang = self.nhap_hang_repo.get_by_id(nhap_hang_id)
        chi_phi = self.chi_phi_service.get_by_ten_chi_phi(nhap_hang_id)
        mat_hang = self.mat_hang_service.get_by_id(nhap_hang.id_mat_hang)
        if nhap_hang is None or chi_phi is None or mat_hang is None:
            return False
        mat_hang.so_luong -= nhap_hang.so_luong
        if not self.mat_hang_service.update(mat_hang.id, mat_hang):
            return False
        if not self.chi_phi_service.delete(chi_phi.id):
            return False
        if not self.nhap_hang_repo.delete(nhap_hang_id):
            return False
        print('Delete nhap hang success')
        print(nhap_hang.to_dict())
        print(chi_phi.to_dict())
        print(mat_hang.to_dict())
        return True
    
    def get_nhap_hang_sort_keys(self):
        return tuple([key for key in NHAP_HANG_SORT_OPTIONS.keys()])
    
    def get_nhap_hang_sort_by_key(self, sort_key):
        value = NHAP_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return NHAP_HANG_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    def get_day_month_year(self) -> dict:
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        return {
            'day': str(now.day),
            'month': str(now.month),
            'year': str(now.year)
        }
    
    def search_mat_hang(self, keyword) -> list[dict]:
        try:
            results = self.mat_hang_search.search(keyword.strip())
            mat_hang_list = []
            if len(results) == 0:
                return []
            if len(results) > 15:
                results = results[0:15]
            for result in results:
                mat_hang = self.mat_hang_service.get_by_id(result['id'])
                if mat_hang is not None:
                    mat_hang_list.append(mat_hang.to_dict())
            return mat_hang_list
        except Exception as e:
            logging.error('Error when search mat hang')
    
    def search_ncc(self, keyword) -> list[str]:
        try:
            results = self.ncc_search.search(keyword.strip())
            if len(results) == 0:
                return []
            if len(results) > 15:
                results = results[0:15]
            return [suggestion['ten_ncc'] for suggestion in results]
        except Exception as e:  
            logging.error('Error when search ncc')
    
    