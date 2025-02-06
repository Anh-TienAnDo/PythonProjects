from datetime import datetime
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
        try:
            sort = sort.strip()
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
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error get_all: %s", e)
            return list()

    def get_by_id(self, khach_hang_id) -> KhachHang:
        return self.khach_hang_repo.get_by_id(khach_hang_id)

    def create(self, khach_hang: KhachHang) -> bool:
        try:
            while self.khach_hang_repo.check_exist_id(khach_hang.id):
                khach_hang.id = GenerationId.generate_id(KHACH_HANG_ID_LENGTH, KHACH_HANG_ID_PREFIX)
            if not self.khach_hang_repo.create(khach_hang):
                return False
            self.search_whoosh.add_or_update_document_ix(khach_hang.id, khach_hang.ten_khach_hang)
            return True
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error create: %s", e)
            return False
        
    def create_many(self, khach_hang_list: list[KhachHang]) -> bool:
        try:
            for khach_hang in khach_hang_list:
                while self.khach_hang_repo.check_exist_id(khach_hang.id):
                    khach_hang.id = GenerationId.generate_id(KHACH_HANG_ID_LENGTH, KHACH_HANG_ID_PREFIX)
            if not self.khach_hang_repo.create_many(khach_hang_list):
                return False
            for khach_hang in khach_hang_list:
                self.search_whoosh.add_or_update_document_ix(khach_hang.id, khach_hang.ten_khach_hang)
            return True
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error create_many: %s", e)
            return False

    def update(self, khach_hang_id, khach_hang: KhachHang) -> bool:
        try:
            if not self.khach_hang_repo.check_exist_id(khach_hang_id):
                return False
            if not self.khach_hang_repo.update(khach_hang_id, khach_hang):
                return False
            self.search_whoosh.add_or_update_document_ix(khach_hang_id, khach_hang.ten_khach_hang)
            return True
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error update: %s", e)
      
    def delete(self, khach_hang_id) -> bool:
        try:
            if not self.khach_hang_repo.check_exist_id(khach_hang_id):
                return False
            if not self.khach_hang_repo.delete(khach_hang_id):
                return False
            self.search_whoosh.delete_document_ix(khach_hang_id)
            return True
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error delete: %s", e)
            return False
    
    def get_khach_hang_sort_keys(self):
        try:
            return tuple([key for key in KHACH_HANG_SORT_OPTIONS.keys()])
        except Exception as e:
            logging.error('Error when get_khach_hang_sort_keys')
            return tuple()
    
    def get_khach_hang_sort_by_key(self, sort_key):
        value = KHACH_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return KHACH_HANG_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    def get_suggestions(self, keyword):
        try:
            results = self.search_whoosh.search(keyword)
            return [suggestion['ten_khach_hang'] for suggestion in results]
        except Exception as e:
            logging.error('Error when get suggestions')
            return list()
        
    def to_list_dict(self, khach_hang_list: list[KhachHang]) -> list[dict]:
        return [khach_hang.to_dict() for khach_hang in khach_hang_list]
    
    def export_data(self, data: list[KhachHang]) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_folder_export()
            if path is None:
                return False
            path = f'{path}/khach_hang_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
            return excel_util.export_data(path, self.to_list_dict(data)) 
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error export_data: %s", e)
            return False
    
    def import_khach_hang(self) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_file_import()
            if path is None:
                return False
            return excel_util.import_khach_hang(path)
        except (ConnectionError, TimeoutError, ValueError) as e:
            logging.error("Error import_khach_hang: %s", e)
            return False