from datetime import datetime
from src.entity.NccEntity import NCC
from src.repository.NccRepo import NCCRepo
from src.config.search_whoosh import SearchWhooshNCC
from src.utils.GenerationId import GenerationId
from src.utils.TextNormalization import TextNormalization
import logging
from contants import NCC_SORT_OPTIONS, NCC_ID_PREFIX, NCC_ID_LENGTH, LIMIT
from concurrent.futures import ThreadPoolExecutor
from src.utils.Decorator import logger, timer

class NCCService:
    def __init__(self):
        self.ncc_repo = NCCRepo()
        self.search_whoosh = SearchWhooshNCC()

    @logger('NCCService')
    @timer('NCCService')
    def get_all(self, sort: str, keyword: str, page: str, limit=LIMIT) -> dict:
        try:
            offset = str((int(page) - 1) * int(limit))
            sort = sort.strip()
            if sort == '' or sort is None or sort not in self.get_ncc_sort_keys():
                sort = 'Tên A-Z'
            sort_by = self.get_ncc_sort_by_key(sort)
            
            if keyword is None or keyword.strip() == '':
                with ThreadPoolExecutor() as executor:
                    futures = [executor.submit(self.ncc_repo.get_all, sort_by, limit, offset),
                                executor.submit(self.ncc_repo.calculate_total)]
                ncc_list, calculate_total = [f.result() for f in futures]
                # ncc_list = self.ncc_repo.get_all(sort_by=sort_by, limit=limit, offset=offset)
                # calculate_total = self.ncc_repo.calculate_total()
                return {
                    'ncc_list': ncc_list,
                    'total_ncc': calculate_total[0] if calculate_total[0] is not None else 0
                }
            keyword = TextNormalization.remove_special_characters(keyword)
            results = self.search_whoosh.search(keyword)
            id_list = [result['id'] for result in results]
            where = f'id IN ({",".join(["?"] * len(id_list))})'
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.ncc_repo.search, sort_by, where, id_list, limit, offset),
                            executor.submit(self.ncc_repo.calculate_total, where, id_list)]
            ncc_list, calculate_total = [f.result() for f in futures]
            # ncc_list = self.ncc_repo.search(sort_by=sort_by, where=where, params=id_list, limit=limit, offset=offset)
            # calculate_total = self.ncc_repo.calculate_total(where=where, params=id_list)
            return {
                'ncc_list': ncc_list,
                'total_ncc': calculate_total[0] if calculate_total[0] is not None else 0
            }
        except Exception as e:
            logging.error('Error when get all NCC %s', e)
            return {
                'ncc_list': [],
                'total_ncc': 0
            }

    @logger('NCCService')
    @timer('NCCService')
    def get_by_id(self, ncc_id) -> NCC:
        return self.ncc_repo.get_by_id(ncc_id)

    @logger('NCCService')
    @timer('NCCService')
    def create(self, ncc: NCC) -> bool:
        try:
            while self.ncc_repo.check_exist_id(ncc.id):
                ncc.id = GenerationId.generate_id(NCC_ID_LENGTH, NCC_ID_PREFIX)
            if not self.ncc_repo.create(ncc):
                return False
            self.search_whoosh.add_or_update_document_ix(ncc.id, ncc.ten_ncc)
            return True
        except Exception as e:
            logging.error('Error when create NCC %s', e)
            return False
        
    @logger('NCCService')
    @timer('NCCService')
    def create_many(self, ncc_list: list[NCC]) -> bool:
        try:
            for index, ncc in enumerate(ncc_list):
                while self.ncc_repo.check_exist_id(ncc_list[index].id):
                    ncc_list[index].id = GenerationId.generate_id(NCC_ID_LENGTH, NCC_ID_PREFIX)
                self.search_whoosh.add_or_update_document_ix(ncc_list[index].id, ncc_list[index].ten_ncc)
            if not self.ncc_repo.create_many(ncc_list):
                return False
            return True
        except Exception as e:
            logging.error('Error when create many NCC %s', e)
            return False

    @logger('NCCService')
    @timer('NCCService')
    def update(self, ncc_id, ncc: NCC) -> bool:
        try:
            # if not self.ncc_repo.check_exist_id(ncc_id):
            #     return False
            if not self.ncc_repo.update(ncc_id, ncc):
                return False
            self.search_whoosh.add_or_update_document_ix(ncc_id, ncc.ten_ncc)
            return True
        except Exception as e:
            logging.error('Error when update NCC %s', e)
            return False
      
    @logger('NCCService')
    @timer('NCCService')
    def delete(self, ncc_id) -> bool:
        try:
            # if not self.ncc_repo.check_exist_id(ncc_id):
            #     return False
            if not self.ncc_repo.delete(ncc_id):
                return False
            self.search_whoosh.delete_document_ix(ncc_id)
            return True
        except Exception as e:
            logging.error('Error when delete NCC %s', e)
            return False
    
    def get_ncc_sort_keys(self):
        return tuple([key for key in NCC_SORT_OPTIONS.keys()])
    
    def get_ncc_sort_by_key(self, sort_key):
        value = NCC_SORT_OPTIONS.get(sort_key)
        if value is None:
            return NCC_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    @logger('NCCService')
    @timer('NCCService')
    def get_suggestions(self, keyword):
        try:
            results = self.search_whoosh.search(keyword)
            return [suggestion['ten_ncc'] for suggestion in results]
        except Exception as e:
            logging.error('Error when get suggestions')
            return list()
        
    def to_list_dict(self, ncc_list: list[NCC]) -> list[dict]:
        return [ncc.to_dict() for ncc in ncc_list]
    
    @logger('NCCService')
    @timer('NCCService')
    def export_data(self, data: list[NCC]) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_folder_export()
            if path is None:
                return False
            path = f'{path}/ncc_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
            return excel_util.export_data(path, self.to_list_dict(data)) 
        except Exception as e:
            logging.error('Error when export NCC %s', e)
            return False
    
    @logger('NCCService')
    @timer('NCCService')
    def import_ncc(self) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_file_import()
            if path is None:
                return False
            return excel_util.import_ncc(path)
        except Exception as e:
            logging.error('Error when import NCC %s', e)
            return False