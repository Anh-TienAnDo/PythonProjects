from src.entity.NccEntity import NCC
from src.repository.NccRepo import NCCRepo
from src.config.search_whoosh import SearchWhooshNCC
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
import logging
from contants import NCC_SORT_OPTIONS, NCC_ID_PREFIX, NCC_ID_LENGTH

class NCCService:
    def __init__(self):
        logging.info('---NCCService initializing---')
        self.ncc_repo = NCCRepo()
        self.search_whoosh = SearchWhooshNCC()

    def get_all(self, sort: str, keyword: str) -> list[NCC]:
        if sort not in self.get_ncc_sort_keys() or sort == '' or sort is None:
            sort = 'Tên A-Z'
        sort_by = self.get_ncc_sort_by_key(sort)
        
        if keyword is None or keyword.strip() == '':
            return self.ncc_repo.get_all(sort_by=sort_by)
        
        keyword = TextNormalization.remove_special_characters(keyword)
        results = self.search_whoosh.search(keyword)
        id_list = [result['id'] for result in results]
        where = f'id IN ({",".join(["?"] * len(id_list))})'
        return self.ncc_repo.search(sort_by=sort_by, where=where, params=id_list)

    def get_by_id(self, ncc_id) -> NCC:
        return self.ncc_repo.get_by_id(ncc_id)

    def create(self, ncc: NCC) -> bool:
        while self.ncc_repo.check_exist_id(ncc.id):
            ncc.id = GenerationId.generate_id(NCC_ID_LENGTH, NCC_ID_PREFIX)
        if not self.ncc_repo.create(ncc):
            return False
        self.search_whoosh.add_or_update_document_ix(ncc.id, ncc.ten_ncc)
        return True

    def update(self, ncc_id, ncc: NCC) -> bool:
        if not self.ncc_repo.check_exist_id(ncc_id):
            return False
        if not self.ncc_repo.update(ncc_id, ncc):
            return False
        self.search_whoosh.add_or_update_document_ix(ncc_id, ncc.ten_ncc)
        return True
      
    def delete(self, ncc_id) -> bool:
        if not self.ncc_repo.check_exist_id(ncc_id):
            return False
        if not self.ncc_repo.delete(ncc_id):
            return False
        self.search_whoosh.delete_document_ix(ncc_id)
        return True
    
    def get_ncc_sort_keys(self):
        return tuple([key for key in NCC_SORT_OPTIONS.keys()])
    
    def get_ncc_sort_by_key(self, sort_key):
        value = NCC_SORT_OPTIONS.get(sort_key)
        if value is None:
            return NCC_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    def get_suggestions(self, keyword):
        try:
            results = self.search_whoosh.search(keyword)
            return [suggestion['ten_ncc'] for suggestion in results]
        except Exception as e:
            logging.error('Error when get suggestions')
            return list()