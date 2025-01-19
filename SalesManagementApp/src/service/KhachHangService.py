from src.entity.KhachHangEntity import KhachHang
from src.repository.KhachHangRepo import KhachHangRepo
from src.config.search_whoosh import SearchWhooshKhachHang
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
import logging
from contants import KHACH_HANG_SORT_OPTIONS, KHACH_HANG_ID_PREFIX, KHACH_HANG_ID_LENGTH

class KhachHangService:
    def __init__(self):
        logging.info('---KhachHangService initializing---')
        self.khach_hang_repo = KhachHangRepo()
        self.search_whoosh = SearchWhooshKhachHang()

    def get_all(self, sort: str, keyword: str) -> list[KhachHang]:
        if sort not in self.get_khach_hang_sort_keys() or sort == '' or sort is None:
            sort = 'Tên A-Z'
        sort_by = self.get_khach_hang_sort_by_key(sort)
        
        if keyword is None or keyword.strip() == '':
            return self.khach_hang_repo.get_all(sort_by=sort_by)
        
        keyword = TextNormalization.remove_special_characters(keyword)
        results = self.search_whoosh.search(keyword)
        id_list = [result['id'] for result in results]
        where = f'id IN ({",".join(["?"] * len(id_list))})'
        return self.khach_hang_repo.search(sort_by=sort_by, where=where, params=id_list)

    def get_by_id(self, khach_hang_id) -> KhachHang:
        return self.khach_hang_repo.get_by_id(khach_hang_id)

    def create(self, khach_hang: KhachHang) -> bool:
        while self.khach_hang_repo.check_exist_id(khach_hang.id):
            khach_hang.id = GenerationId.generate_id(KHACH_HANG_ID_LENGTH, KHACH_HANG_ID_PREFIX)
        if not self.khach_hang_repo.create(khach_hang):
            return False
        self.search_whoosh.add_or_update_document_ix(khach_hang.id, khach_hang.ten_khach_hang)
        return True

    def update(self, khach_hang_id, khach_hang: KhachHang) -> bool:
        if not self.khach_hang_repo.check_exist_id(khach_hang_id):
            return False
        if not self.khach_hang_repo.update(khach_hang_id, khach_hang):
            return False
        self.search_whoosh.add_or_update_document_ix(khach_hang_id, khach_hang.ten_khach_hang)
        return True
      
    def delete(self, khach_hang_id) -> bool:
        if not self.khach_hang_repo.check_exist_id(khach_hang_id):
            return False
        if not self.khach_hang_repo.delete(khach_hang_id):
            return False
        self.search_whoosh.delete_document_ix(khach_hang_id)
        return True
    
    def get_khach_hang_sort_keys(self):
        return tuple([key for key in KHACH_HANG_SORT_OPTIONS.keys()])
    
    def get_khach_hang_sort_by_key(self, sort_key):
        return KHACH_HANG_SORT_OPTIONS[sort_key]
    
    def get_suggestions(self, keyword):
        try:
            results = self.search_whoosh.search(keyword)
            return [suggestion['ten_khach_hang'] for suggestion in results]
        except Exception as e:
            logging.error('Error when get suggestions')
            return list()