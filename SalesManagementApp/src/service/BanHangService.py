from src.entity.BanHangEntity import BanHang
from src.repository.BanHangRepo import BanHangRepo
from src.service.MatHangService import MatHangService
from src.config.search_whoosh import SearchWhooshMatHang, SearchWhooshKhachHang
from src.utils.GenerationId import GenerationId
import logging
from contants import BAN_HANG_SORT_OPTIONS, BAN_HANG_ID_PREFIX, BAN_HANG_ID_LENGTH, REPORT_BAN_HANG_SORT_OPTIONS, REPORT_BAN_HANG_DETAIL_SORT_OPTIONS, LIMIT
from datetime import datetime

class BanHangService:
    def __init__(self):
        logging.info('---BanHangService initializing---')
        self.ban_hang_repo = BanHangRepo()
        self.mat_hang_search = SearchWhooshMatHang()
        self.khach_hang_search = SearchWhooshKhachHang()
        self.mat_hang_service = MatHangService()

    def get_all(self, sort: str, day: str, month: str, year: str, page: str, limit=LIMIT) -> dict:
        try:
            offset = str((int(page) - 1) * int(limit))
            sort = sort.strip()
            if sort not in self.get_ban_hang_sort_keys() or sort == '' or sort is None:
                sort = 'Tên A-Z'
            sort_by = self.get_ban_hang_sort_by_key(sort)
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
                where = f"strftime('%m-%Y', ngay_ban) = '{month}-{year}'"
            else:
                if len(day) == 1:
                    day = f'0{day}'
                where = f"strftime('%d-%m-%Y', ngay_ban) = '{day}-{month}-{year}'"
            ban_hang_list = self.ban_hang_repo.get_all(sort_by, where, limit, offset)
            calculate_total = self.ban_hang_repo.calculate_total(where)
            return {
                'ban_hang_list': ban_hang_list,
                'total_ban_hang': calculate_total[0] if calculate_total[0] is not None else 0,
                'total_so_luong': calculate_total[1] if calculate_total[1] is not None else 0,
                'total_thanh_tien': calculate_total[2] if calculate_total[2] is not None else 0
            }
        except Exception as e:
            logging.error('Error when get all ban hang %s', e)
            return {
                'ban_hang_list': [],
                'total_ban_hang': 0,
                'total_so_luong': 0,
                'total_thanh_tien': 0
            }
    
    def report(self, sort: str, day: str, month: str, year: str) -> list:
        try:
            sort = sort.strip()
            if sort not in self.get_report_ban_hang_sort_keys() or sort == '' or sort is None:
                sort = 'Tổng tiền nhiều - ít'
            sort_by = self.get_report_ban_hang_sort_by_key(sort)
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
                where = f"strftime('%m-%Y', ngay_ban) = '{month}-{year}'"
            else:
                if len(day) == 1:
                    day = f'0{day}'
                where = f"strftime('%d-%m-%Y', ngay_ban) = '{day}-{month}-{year}'"
            return self.ban_hang_repo.report(sort_by, where)
        except Exception as e:
            logging.error('Error when report ban hang %s', e)
            return []
    
    def report_detail_mat_hang(self, sort: str, month: str, year: str, id_mat_hang: str) -> list:
        try:
            sort = sort.strip()
            if sort not in self.get_report_ban_hang_detail_sort_keys() or sort == '' or sort is None:
                sort = 'Ngày bán mới - cũ'
            sort_by = self.get_report_ban_hang_detail_sort_by_key(sort)
            month = month.strip()
            year = year.strip()
            now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            if month is None or month == '':
                month = str(now.month)
            if year is None or year == '':
                year = str(now.year)
            if len(month) == 1:
                month = f'0{month}'
            where = f"strftime('%m-%Y', ngay_ban) = '{month}-{year}' AND id_mat_hang = '{id_mat_hang}'"
            return self.ban_hang_repo.report_detail_mat_hang(sort_by, where)
        except Exception as e:
            logging.error('Error when report detail mat hang %s', e)
            return []
        
    def get_by_id(self, ban_hang_id) -> BanHang:
        return self.ban_hang_repo.get_by_id(ban_hang_id)

    def create(self, ban_hang: BanHang) -> bool:
        while self.ban_hang_repo.check_exist_id(ban_hang.id):
            ban_hang.id = GenerationId.generate_id(BAN_HANG_ID_LENGTH, BAN_HANG_ID_PREFIX)
        try:
            ban_hang.thanh_tien = ban_hang.so_luong * ban_hang.gia_ban
            self.ban_hang_repo.create(ban_hang)
            mat_hang = self.mat_hang_service.get_by_id(ban_hang.id_mat_hang)
            mat_hang.so_luong -= ban_hang.so_luong
            self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            return True
        except Exception as e:
            logging.error('Error when create ban hang %s', e)
            return False
        
    def create_many(self, ban_hang_list: list[BanHang]) -> bool:
        for index, ban_hang in enumerate(ban_hang_list):
            try:
                while self.ban_hang_repo.check_exist_id(ban_hang_list[index].id):
                    ban_hang_list[index].id = GenerationId.generate_id(BAN_HANG_ID_LENGTH, BAN_HANG_ID_PREFIX)
                ban_hang_list[index].thanh_tien = ban_hang.so_luong * ban_hang.gia_ban
                mat_hang = self.mat_hang_service.get_by_id(ban_hang.id_mat_hang)
                mat_hang.so_luong -= ban_hang.so_luong
                self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            except Exception as e:
                logging.error('Error when create many ban hang %s', e)
        try:
            return self.ban_hang_repo.create_many(ban_hang_list)
        except Exception as e:
            logging.error('Error when create many ban hang %s', e)
            return False

    def update(self, ban_hang_id, ban_hang: BanHang, so_luong_ban_old: int) -> bool:
        try: 
            if not self.ban_hang_repo.check_exist_id(ban_hang_id):
                return False
            ban_hang.thanh_tien = ban_hang.so_luong * ban_hang.gia_ban
            self.ban_hang_repo.update(ban_hang_id, ban_hang)
            mat_hang = self.mat_hang_service.get_by_id(ban_hang.id_mat_hang)
            mat_hang.so_luong = mat_hang.so_luong + so_luong_ban_old - ban_hang.so_luong
            self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            return True
        except Exception as e:
            logging.error('Error when update ban hang %s', e)
            return False
      
    def delete(self, ban_hang_id) -> bool:
        try:
            if not self.ban_hang_repo.check_exist_id(ban_hang_id):
                return False
            ban_hang = self.ban_hang_repo.get_by_id(ban_hang_id)
            self.ban_hang_repo.delete(ban_hang_id)
            mat_hang = self.mat_hang_service.get_by_id(ban_hang.id_mat_hang)
            mat_hang.so_luong += ban_hang.so_luong
            self.mat_hang_service.update_so_luong(mat_hang.id, mat_hang.so_luong)
            return True
        except Exception as e:
            logging.error('Error when delete ban hang %s', e)
            return False
    
    def get_ban_hang_sort_keys(self):
        try:
            return tuple([key for key in BAN_HANG_SORT_OPTIONS.keys()])
        except Exception as e:
            logging.error('Error when get ban hang sort keys %s', e)
            return []
    
    def get_ban_hang_sort_by_key(self, sort_key):
        value = BAN_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return BAN_HANG_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    def get_report_ban_hang_sort_keys(self):
        try:
            return tuple([key for key in REPORT_BAN_HANG_SORT_OPTIONS.keys()])
        except Exception as e:
            logging.error('Error when get report ban hang sort keys %s', e)
            return []
    
    def get_report_ban_hang_sort_by_key(self, sort_key):
        value = REPORT_BAN_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return REPORT_BAN_HANG_SORT_OPTIONS.get('Tổng tiền nhiều - ít')
        return value
    
    def get_report_ban_hang_detail_sort_keys(self):
        try:
            return tuple([key for key in REPORT_BAN_HANG_DETAIL_SORT_OPTIONS.keys()])
        except Exception as e:
            logging.error('Error when get report ban hang detail sort keys %s', e)
            return []
    
    def get_report_ban_hang_detail_sort_by_key(self, sort_key):
        value = REPORT_BAN_HANG_DETAIL_SORT_OPTIONS.get(sort_key)
        if value is None:
            return REPORT_BAN_HANG_DETAIL_SORT_OPTIONS.get('Ngày bán mới - cũ')
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
            logging.error('Error when search mat hang %s', e)
            return []
    
    def search_khach_hang(self, keyword) -> list[str]:
        try:
            results = self.khach_hang_search.search(keyword.strip())
            if len(results) == 0:
                return []
            if len(results) > 15:
                results = results[0:15]
            return [suggestion['ten_khach_hang'] for suggestion in results]
        except Exception as e:  
            logging.error('Error when search khach_hang %s', e)
            return []
        
    def to_list_dict(self, ban_hang_list: list[BanHang]) -> list[dict]:
        return [ban_hang.to_dict() for ban_hang in ban_hang_list]
    
    def export_data(self, data: list[BanHang]) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_folder_export()
            if path is None:
                return False
            path = f'{path}/ban_hang_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
            return excel_util.export_data(path, self.to_list_dict(data)) 
        except Exception as e:
            logging.error('Error when export data %s', e)
            return False
    
    def import_ban_hang(self) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_file_import()
            if path is None:
                return False
            return excel_util.import_ban_hang(path)
        except Exception as e:
            logging.error('Error when import ban hang %s', e)
            return False
    
    