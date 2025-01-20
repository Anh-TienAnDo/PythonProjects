from src.entity.NhapHangEntity import NhapHang
from src.repository.NhapHangRepo import NhapHangRepo
from src.utils.GenerationId import GenerationId
import logging
from contants import NHAP_HANG_SORT_OPTIONS, NHAP_HANG_ID_PREFIX, NHAP_HANG_ID_LENGTH
from datetime import datetime

class NhapHangService:
    def __init__(self):
        logging.info('---NhapHangService initializing---')
        self.nhap_hang_repo = NhapHangRepo()

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
        print(where)
        return self.nhap_hang_repo.get_all(sort_by, where)
        
    def get_by_id(self, nhap_hang_id) -> NhapHang:
        return self.nhap_hang_repo.get_by_id(nhap_hang_id)

    def create(self, nhap_hang: NhapHang) -> bool:
        while self.nhap_hang_repo.check_exist_id(nhap_hang.id):
            nhap_hang.id = GenerationId.generate_id(NHAP_HANG_ID_LENGTH, NHAP_HANG_ID_PREFIX)
        return self.nhap_hang_repo.create(nhap_hang)

    def update(self, nhap_hang_id, nhap_hang: NhapHang) -> bool:
        if not self.nhap_hang_repo.check_exist_id(nhap_hang_id):
            return False
        return self.nhap_hang_repo.update(nhap_hang_id, nhap_hang)
      
    def delete(self, nhap_hang_id) -> bool:
        if not self.nhap_hang_repo.check_exist_id(nhap_hang_id):
            return False
        return self.nhap_hang_repo.delete(nhap_hang_id)
    
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