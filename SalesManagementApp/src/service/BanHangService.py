from src.entity.BanHangEntity import BanHang
from src.repository.BanHangRepo import BanHangRepo
from src.service.MatHangService import MatHangService
from src.config.search_whoosh import SearchWhooshMatHang, SearchWhooshKhachHang
from src.utils.GenerationId import GenerationId
import logging
from contants import BAN_HANG_SORT_OPTIONS, BAN_HANG_ID_PREFIX, BAN_HANG_ID_LENGTH
from datetime import datetime

class BanHangService:
    def __init__(self):
        logging.info('---BanHangService initializing---')
        self.ban_hang_repo = BanHangRepo()
        self.mat_hang_search = SearchWhooshMatHang()
        self.khach_hang_search = SearchWhooshKhachHang()
        self.mat_hang_service = MatHangService()

    def get_all(self, sort: str, day: str, month: str, year: str) -> list[BanHang]:
        sort = sort.strip()
        if sort not in self.get_ban_hang_sort_keys() or sort == '' or sort is None:
            sort = 'Tên A-Z'
        sort_by = self.get_ban_hang_sort_by_key(sort)

        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        if month is None or month.strip() == '':
            month = str(now.month)
        if year is None or year.strip() == '':
            year = str(now.year)
        if len(month) == 1:
            month = f'0{month}'
        if day is None or day.strip() == '':
            where = f"strftime('%m-%Y', ngay_ban) = '{month}-{year}'"
        else:
            if len(day) == 1:
                day = f'0{day}'
            where = f"strftime('%d-%m-%Y', ngay_ban) = '{day}-{month}-{year}'"
        return self.ban_hang_repo.get_all(sort_by, where)
        
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
            self.mat_hang_service.update(mat_hang.id, mat_hang)
            print('Create ban hang success')
            print(ban_hang.to_dict())
            print(mat_hang.to_dict())
            return True
        except Exception as e:
            logging.error('Error when create ban hang')
            return False

    def update(self, ban_hang_id, ban_hang: BanHang, so_luong_ban_old: int) -> bool:
        if not self.ban_hang_repo.check_exist_id(ban_hang_id):
            return False
        try: 
            ban_hang.thanh_tien = ban_hang.so_luong * ban_hang.gia_ban
            self.ban_hang_repo.update(ban_hang_id, ban_hang)
            mat_hang = self.mat_hang_service.get_by_id(ban_hang.id_mat_hang)
            mat_hang.so_luong = mat_hang.so_luong + so_luong_ban_old - ban_hang.so_luong
            self.mat_hang_service.update(mat_hang.id, mat_hang)
            print('Update ban hang success')
            print(ban_hang.to_dict())
            print(mat_hang.to_dict())
            return True
        except Exception as e:
            logging.error('Error when update ban hang')
            return False
      
    def delete(self, ban_hang_id) -> bool:
        if not self.ban_hang_repo.check_exist_id(ban_hang_id):
            return False
        ban_hang = self.ban_hang_repo.get_by_id(ban_hang_id)
        mat_hang = self.mat_hang_service.get_by_id(ban_hang.id_mat_hang)
        mat_hang.so_luong += ban_hang.so_luong
        try:
            self.ban_hang_repo.delete(ban_hang_id)
            self.mat_hang_service.update(mat_hang.id, mat_hang)
            print('Delete ban hang success')
            print(ban_hang.to_dict())
            print(mat_hang.to_dict())
            return True
        except Exception as e:
            logging.error('Error when delete ban hang')
            return False
    
    def get_ban_hang_sort_keys(self):
        return tuple([key for key in BAN_HANG_SORT_OPTIONS.keys()])
    
    def get_ban_hang_sort_by_key(self, sort_key):
        value = BAN_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return BAN_HANG_SORT_OPTIONS.get('Tên A-Z')
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
    
    def search_khach_hang(self, keyword) -> list[str]:
        try:
            results = self.khach_hang_search.search(keyword.strip())
            if len(results) == 0:
                return []
            if len(results) > 15:
                results = results[0:15]
            return [suggestion['ten_khach_hang'] for suggestion in results]
        except Exception as e:  
            logging.error('Error when search khach_hang')
            return []
    
    