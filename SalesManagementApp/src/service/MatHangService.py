from src.entity.MatHangEntity import MatHang
from src.repository.MatHangRepo import MatHangRepo
from src.utils.GenerationId import GenerationId
import logging
from contants import MAT_HANG_SORT_OPTIONS, MAT_HANG_ID_PREFIX, MAT_HANG_ID_LENGTH, MAT_HANG_TABLE

class MatHangService:
    def __init__(self):
        logging.info('---MatHangService initializing---')
        self.mat_hang_repo = MatHangRepo()

    def get_all(self, sort: str) -> list[MatHang]:
        if sort not in self.get_mat_hang_sort_keys() or sort == '' or sort is None:
            sort = 'Tên A-Z'
        sort_by = self.get_mat_hang_sort_by_key(sort)
        return self.mat_hang_repo.get_all(sort_by=sort_by)

    def get_by_id(self, mat_hang_id) -> MatHang:
        return self.mat_hang_repo.get_by_id(mat_hang_id)

    def create(self, mat_hang: MatHang) -> bool:
        while self.mat_hang_repo.check_exist_id(mat_hang.id):
            mat_hang.id = GenerationId.generate_id(MAT_HANG_ID_LENGTH, MAT_HANG_ID_PREFIX)
        
        return self.mat_hang_repo.create(mat_hang)

    def update(self, mat_hang_id, mat_hang: MatHang) -> bool:
        return self.mat_hang_repo.update(mat_hang_id, mat_hang)
      
    def delete(self, mat_hang_id) -> bool:
        return self.mat_hang_repo.delete(mat_hang_id)
    
    def get_mat_hang_sort_keys(self):
        return tuple([key for key in MAT_HANG_SORT_OPTIONS.keys()])
    
    def get_mat_hang_sort_by_key(self, sort_key):
        return MAT_HANG_SORT_OPTIONS[sort_key]