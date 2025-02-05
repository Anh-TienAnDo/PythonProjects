from datetime import datetime
from src.entity.MatHangEntity import MatHang
from src.repository.MatHangRepo import MatHangRepo
from src.config.search_whoosh import SearchWhooshMatHang
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
import logging
from contants import MAT_HANG_SORT_OPTIONS, MAT_HANG_ID_PREFIX, MAT_HANG_ID_LENGTH
from src.utils.Excel import Excel

class MatHangService:
    def __init__(self):
        logging.info('---MatHangService initializing---')
        self.mat_hang_repo = MatHangRepo()
        self.search_whoosh = SearchWhooshMatHang()
        self.excel_util = Excel()

    def get_all(self, sort: str, keyword: str) -> list[MatHang]:
        sort = sort.strip()
        if sort not in self.get_mat_hang_sort_keys() or sort == '' or sort is None:
            sort = 'Tên A-Z'
        sort_by = self.get_mat_hang_sort_by_key(sort)
        
        if keyword is None or keyword.strip() == '':
            return self.mat_hang_repo.get_all(sort_by=sort_by)
        
        keyword = TextNormalization.remove_special_characters(keyword)
        results = self.search_whoosh.search(keyword)
        id_list = [result['id'] for result in results]
        where = f'id IN ({",".join(["?"] * len(id_list))})'
        return self.mat_hang_repo.search(sort_by=sort_by, where=where, params=id_list)

    def get_by_id(self, mat_hang_id) -> MatHang:
        return self.mat_hang_repo.get_by_id(mat_hang_id)

    def create(self, mat_hang: MatHang) -> bool:
        while self.mat_hang_repo.check_exist_id(mat_hang.id):
            mat_hang.id = GenerationId.generate_id(MAT_HANG_ID_LENGTH, MAT_HANG_ID_PREFIX)
        if not self.mat_hang_repo.create(mat_hang):
            return False
        self.search_whoosh.add_or_update_document_ix(mat_hang.id, mat_hang.ten_hang)
        return True

    def update(self, mat_hang_id, mat_hang: MatHang) -> bool:
        if not self.mat_hang_repo.check_exist_id(mat_hang_id):
            return False
        if not self.mat_hang_repo.update(mat_hang_id, mat_hang):
            return False
        self.search_whoosh.add_or_update_document_ix(mat_hang_id, mat_hang.ten_hang)
        return True
    
    def update_so_luong(self, mat_hang_id, so_luong: int) -> bool:
        if not self.mat_hang_repo.check_exist_id(mat_hang_id):
            return False
        if not self.mat_hang_repo.update_so_luong(mat_hang_id, so_luong):
            return False
        return True
      
    def delete(self, mat_hang_id) -> bool:
        if not self.mat_hang_repo.check_exist_id(mat_hang_id):
            return False
        if not self.mat_hang_repo.delete(mat_hang_id):
            return False
        self.search_whoosh.delete_document_ix(mat_hang_id)
        return True
    
    def get_mat_hang_sort_keys(self):
        return tuple([key for key in MAT_HANG_SORT_OPTIONS.keys()])
    
    def get_mat_hang_sort_by_key(self, sort_key):
        value = MAT_HANG_SORT_OPTIONS.get(sort_key)
        if value is None:
            return MAT_HANG_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    def get_suggestions(self, keyword):
        try:
            results = self.search_whoosh.search(keyword)
            return [suggestion['ten_mat_hang'] for suggestion in results]
        except Exception as e:
            logging.error('Error when get suggestions')
            return list()
        
    def to_list_dict(self, mat_hang_list: list[MatHang]) -> list[dict]:
        return [mat_hang.to_dict() for mat_hang in mat_hang_list]
    
    def export_data(self, data: list[MatHang]) -> bool:
        data = self.to_list_dict(data)
        path = self.excel_util.select_folder_export()
        if path is None:
            return False
        path = f'{path}/mat_hang_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
        return self.excel_util.export_data(path, data) 
    
    def import_mat_hang(self) -> bool:
        path = self.excel_util.select_file_import()
        if path is None:
            return False
        return self.excel_util.import_mat_hang(path)