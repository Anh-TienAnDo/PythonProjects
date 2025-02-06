from src.entity.NhapHangEntity import NhapHang
from src.repository.NhapHangRepo import NhapHangRepo
from src.service.MatHangService import MatHangService
from src.config.search_whoosh import SearchWhooshMatHang, SearchWhooshNCC
from src.utils.GenerationId import GenerationId
import logging
from contants import NHAP_HANG_SORT_OPTIONS, NHAP_HANG_ID_PREFIX, NHAP_HANG_ID_LENGTH, REPORT_NHAP_HANG_SORT_OPTIONS, REPORT_NHAP_HANG_DETAIL_SORT_OPTIONS
from datetime import datetime

class NhapHangService:
    def __init__(self):
        logging.info('---NhapHangService initializing---')
        self.nhap_hang_repo = NhapHangRepo()
        self.mat_hang_search = SearchWhooshMatHang()
        self.ncc_search = SearchWhooshNCC()
        self.mat_hang_service = MatHangService()

    def get_all(self, sort: str, day: str, month: str, year: str) -> list[NhapHang]:
        try:
            sort = sort.strip()
            if sort not in self.get_nhap_hang_sort_keys() or sort == '' or sort is None:
                sort = 'Tên A-Z'
            sort_by = self.get_nhap_hang_sort_by_key(sort)
            day = day.strip()
            month = month.strip()
            year = year.strip()
            now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            if month is None or month == '':
                month = str(now.month)
            if year is None or year == '':
                year = str(now.year)
            if len(month) == 1:
                month = f'0{month}'
            if day is None or day == '':
                where = f"strftime('%m-%Y', ngay_nhap) = '{month}-{year}'"
            else:
                if len(day) == 1:
                    day = f'0{day}'
                where = f"strftime('%d-%m-%Y', ngay_nhap) = '{day}-{month}-{year}'"
            return self.nhap_hang_repo.get_all(sort_by, where)
        except Exception as e:
            logging.error('Error when get all nhap hang %s', e)
            return list()
    
    def report(self, sort: str, day: str, month: str, year: str) -> list:
        try:
            sort = sort.strip()
            if sort not in self.get_report_nhap_hang_sort_keys() or sort == '' or sort is None:
                sort = 'Tổng tiền nhiều - ít'
            sort_by = self.get_report_nhap_hang_sort_by_key(sort)
            day = day.strip()
            month = month.strip()
            year = year.strip()
            now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            if month is None or month == '':
                month = str(now.month)
            if year is None or year == '':
                year = str(now.year)
            if len(month) == 1:
                month = f'0{month}'
            if day is None or day == '':
                where = f"strftime('%m-%Y', ngay_nhap) = '{month}-{year}'"
            else:
                if len(day) == 1:
                    day = f'0{day}'
                where = f"strftime('%d-%m-%Y', ngay_nhap) = '{day}-{month}-{year}'"
            return self.nhap_hang_repo.report(sort_by, where)
        except Exception as e:
            logging.error('Error when report nhap hang %s', e)
            return list()
    
    def report_detail_mat_hang(self, sort: str, month: str, year: str, id_mat_hang: str) -> list:
        try:
            sort = sort.strip()
            if sort not in self.get_report_nhap_hang_detail_sort_keys() or sort == '' or sort is None:
                sort = 'Ngày bán mới - cũ'
            sort_by = self.get_report_nhap_hang_detail_sort_by_key(sort)
            month = month.strip()
            year = year.strip()
            now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            if month is None or month == '':
                month = str(now.month)
            if year is None or year == '':
                year = str(now.year)
            if len(month) == 1:
                month = f'0{month}'
            where = f"strftime('%m-%Y', ngay_nhap) = '{month}-{year}' AND id_mat_hang = '{id_mat_hang}'"
            return self.nhap_hang_repo.report_detail_nhap_hang(sort_by, where)
        except Exception as e:
            logging.error('Error when report detail nhap hang %s', e)
            return list()
        
    def get_by_id(self, nhap_hang_id) -> NhapHang:
        return self.nhap_hang_repo.get_by_id(nhap_hang_id)

    def create(self, nhap_hang: NhapHang) -> bool:
        while self.nhap_hang_repo.check_exist_id(nhap_hang.id):
            nhap_hang.id = GenerationId.generate_id(NHAP_HANG_ID_LENGTH, NHAP_HANG_ID_PREFIX)
        try:
            nhap_hang.thanh_tien = nhap_hang.so_luong * nhap_hang.gia_nhap
            self.nhap_hang_repo.create(nhap_hang)
            mat_hang = self.mat_hang_service.get_by_id(nhap_hang.id_mat_hang)
            mat_hang.so_luong += nhap_hang.so_luong
            self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            return True
        except Exception as e:
            logging.error('Error when create nhap hang')
            return False
        
    def create_many(self, nhap_hang_list: list[NhapHang]) -> bool:
        for index, nhap_hang in enumerate(nhap_hang_list):
            try:
                while self.nhap_hang_repo.check_exist_id(nhap_hang.id):
                    nhap_hang_list[index].id = GenerationId.generate_id(NHAP_HANG_ID_LENGTH, NHAP_HANG_ID_PREFIX)
                nhap_hang_list[index].thanh_tien = nhap_hang.so_luong * nhap_hang.gia_nhap
                mat_hang = self.mat_hang_service.get_by_id(nhap_hang.id_mat_hang)
                mat_hang.so_luong += nhap_hang.so_luong
                self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            except Exception as e:
                logging.error('Error when create many ban hang %s', e)
        try:
            return self.nhap_hang_repo.create_many(nhap_hang_list)
        except Exception as e:
            logging.error('Error when create many ban hang %s', e)
            return False

    def update(self, nhap_hang_id, nhap_hang: NhapHang, so_luong_nhap_old: int) -> bool:
        try: 
            if not self.nhap_hang_repo.check_exist_id(nhap_hang_id):
                return False
            nhap_hang.thanh_tien = nhap_hang.so_luong * nhap_hang.gia_nhap
            self.nhap_hang_repo.update(nhap_hang_id, nhap_hang)
            mat_hang = self.mat_hang_service.get_by_id(nhap_hang.id_mat_hang)
            mat_hang.so_luong = mat_hang.so_luong - so_luong_nhap_old + nhap_hang.so_luong
            self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            return True
        except Exception as e:
            logging.error('Error when update nhap hang')
            return False
      
    def delete(self, nhap_hang_id) -> bool:
        try:
            if not self.nhap_hang_repo.check_exist_id(nhap_hang_id):
                return False
            nhap_hang = self.nhap_hang_repo.get_by_id(nhap_hang_id)
            self.nhap_hang_repo.delete(nhap_hang_id)
            mat_hang = self.mat_hang_service.get_by_id(nhap_hang.id_mat_hang)
            mat_hang.so_luong -= nhap_hang.so_luong
            self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            return True
        except Exception as e:
            logging.error('Error when delete nhap hang')
            return False
    
    def get_nhap_hang_sort_keys(self):
        return tuple([key for key in NHAP_HANG_SORT_OPTIONS.keys()])
    
    def get_nhap_hang_sort_by_key(self, sort_key):
        value = NHAP_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return NHAP_HANG_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    def get_report_nhap_hang_sort_keys(self):
        return tuple([key for key in REPORT_NHAP_HANG_SORT_OPTIONS.keys()])
    
    def get_report_nhap_hang_sort_by_key(self, sort_key):
        value = REPORT_NHAP_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return REPORT_NHAP_HANG_SORT_OPTIONS.get('Tổng tiền nhiều - ít')
        return value
    
    def get_report_nhap_hang_detail_sort_keys(self):
        return tuple([key for key in REPORT_NHAP_HANG_DETAIL_SORT_OPTIONS.keys()])
    
    def get_report_nhap_hang_detail_sort_by_key(self, sort_key):
        value = REPORT_NHAP_HANG_DETAIL_SORT_OPTIONS.get(sort_key)
        if value is None:
            return REPORT_NHAP_HANG_DETAIL_SORT_OPTIONS.get('Ngày nhập mới - cũ')
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
            return []
    
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
            return []
    
    def to_list_dict(self, nhap_hang_list: list[NhapHang]) -> list[dict]:
        return [nhap_hang.to_dict() for nhap_hang in nhap_hang_list]
    
    def export_data(self, data: list[NhapHang]) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_folder_export()
            if path is None:
                return False
            path = f'{path}/nhap_hang_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
            return excel_util.export_data(path, self.to_list_dict(data)) 
        except Exception as e:
            logging.error('Error when export data %s', e)
            return False
    
    def import_nhap_hang(self) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_file_import()
            if path is None:
                return False
            return excel_util.import_nhap_hang(path)
        except Exception as e:
            logging.error('Error when import nhap hang %s', e)
            return False