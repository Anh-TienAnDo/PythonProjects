from datetime import datetime
from src.entity.MatHangEntity import MatHang
from src.repository.MatHangRepo import MatHangRepo
from src.config.search_whoosh import SearchWhooshMatHang
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
import logging
from contants import MAT_HANG_SORT_OPTIONS, MAT_HANG_ID_PREFIX, MAT_HANG_ID_LENGTH, LIMIT

class MatHangService:
    def __init__(self):
        logging.info('---MatHangService initializing---')
        self.mat_hang_repo = MatHangRepo()
        self.search_whoosh = SearchWhooshMatHang()

    def get_all(self, sort: str, keyword: str, page: str, limit=LIMIT) -> dict:
        try:
            offset = str((int(page) - 1) * int(limit))
            sort = sort.strip()
            if sort == '' or sort is None or sort not in self.get_mat_hang_sort_keys():
                sort = 'Tên A-Z'
            sort_by = self.get_mat_hang_sort_by_key(sort)
            
            if keyword is None or keyword.strip() == '':
                mat_hang_list = self.mat_hang_repo.get_all(sort_by=sort_by, limit=limit, offset=offset)
                calculate_total = self.mat_hang_repo.calculate_total()
                return {
                    'mat_hang_list': mat_hang_list,
                    'total_mat_hang': calculate_total[0],
                    'total_so_luong': calculate_total[1]
                }
            keyword = TextNormalization.remove_special_characters(keyword)
            results = self.search_whoosh.search(keyword)
            id_list = [result['id'] for result in results]
            where = f'id IN ({",".join(["?"] * len(id_list))})'
            mat_hang_list = self.mat_hang_repo.search(sort_by=sort_by, where=where, params=id_list, limit=limit, offset=offset)
            calculate_total = self.mat_hang_repo.calculate_total(where=where, params=id_list)
            return {
                'mat_hang_list': mat_hang_list,
                'total_mat_hang': calculate_total[0],
                'total_so_luong': calculate_total[1],
                
            }
        except Exception as e:
            logging.error('Error when get all mat hang %s', e)
            return {
                'mat_hang_list': [],
                'total_mat_hang': 0,
                'total_so_luong': 0
            }

    def get_by_id(self, mat_hang_id) -> MatHang:
        return self.mat_hang_repo.get_by_id(mat_hang_id)

    def create(self, mat_hang: MatHang) -> bool:
        try:
            while self.mat_hang_repo.check_exist_id(mat_hang.id):
                mat_hang.id = GenerationId.generate_id(MAT_HANG_ID_LENGTH, MAT_HANG_ID_PREFIX)
            if not self.mat_hang_repo.create(mat_hang):
                return False
            self.search_whoosh.add_or_update_document_ix(mat_hang.id, mat_hang.ten_hang)
            return True
        except Exception as e:
            logging.error('Error when create mat hang %s', e)
            return False
        
    def create_many(self, mat_hang_list: list[MatHang]) -> bool:
        try:
            for mat_hang in mat_hang_list:
                while self.mat_hang_repo.check_exist_id(mat_hang.id):
                    mat_hang.id = GenerationId.generate_id(MAT_HANG_ID_LENGTH, MAT_HANG_ID_PREFIX)
            if not self.mat_hang_repo.create_many(mat_hang_list):
                return False
            for mat_hang in mat_hang_list:
                self.search_whoosh.add_or_update_document_ix(mat_hang.id, mat_hang.ten_hang)
            return True
        except Exception as e:
            logging.error('Error when create many mat hang %s', e)
            return False

    def update(self, mat_hang_id, mat_hang: MatHang) -> bool:
        try:
            # if not self.mat_hang_repo.check_exist_id(mat_hang_id):
            #     return False
            if not self.mat_hang_repo.update(mat_hang_id, mat_hang):
                return False
            self.search_whoosh.add_or_update_document_ix(mat_hang_id, mat_hang.ten_hang)
            return True
        except Exception as e:
            logging.error('Error when update mat hang %s', e)
            return False
    
    def update_so_luong(self, mat_hang_id, so_luong: int) -> bool:
        try:
            # if not self.mat_hang_repo.check_exist_id(mat_hang_id):
            #     return False
            if not self.mat_hang_repo.update_so_luong(mat_hang_id, so_luong):
                return False
            return True
        except Exception as e:
            logging.error('Error when update so luong mat hang %s', e)
            return False
      
    def delete(self, mat_hang_id) -> bool:
        try:
            # if not self.mat_hang_repo.check_exist_id(mat_hang_id):
            #     return False
            if not self.mat_hang_repo.delete(mat_hang_id):
                return False
            self.search_whoosh.delete_document_ix(mat_hang_id)
            return True
        except Exception as e:
            logging.error('Error when delete mat hang %s', e)
            return False
    
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
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            data = self.to_list_dict(data)
            path = excel_util.select_folder_export()
            if path is None:
                return False
            path = f'{path}/mat_hang_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
            return excel_util.export_data(path, data) 
        except Exception as e:
            logging.error('Error when export data %s', e)
            return False
    
    def import_mat_hang(self) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try: 
            path = excel_util.select_file_import()
            if path is None:
                return False
            return excel_util.import_mat_hang(path)
        except Exception as e:
            logging.error('Error when import mat hang %s', e)
            return False