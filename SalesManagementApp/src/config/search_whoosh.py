from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from contants import WHOOSH_INDEX_DIR, WHOOSH_PATH, MAT_HANG_SORT_OPTIONS
import os
from src.utils.Decorator import logger, timer

class SearchWhoosh:
    def __init__(self):
        self.index_dir = WHOOSH_INDEX_DIR
        
class SearchWhooshMatHang(SearchWhoosh):
    @logger('SearchWhooshMatHang')
    @timer('SearchWhooshMatHang')
    def __init__(self):
        super().__init__()
        self.schema_mat_hang = Schema(
            id=ID(stored=True, unique=True),
            ten_mat_hang=TEXT(stored=True)
        )
        self.ix_mat_hang = None
        self.index_name_mat_hang = "mat_hang"
        self.create_index()
        
    def create_index(self):
        if not os.path.exists(WHOOSH_PATH):
            os.mkdir(WHOOSH_PATH)
        if not exists_in(WHOOSH_PATH, indexname=self.index_name_mat_hang):
            self.ix_mat_hang = create_in(WHOOSH_PATH, self.schema_mat_hang, indexname=self.index_name_mat_hang)
        else:
            self.ix_mat_hang = open_dir(WHOOSH_PATH, indexname=self.index_name_mat_hang)
            
    @logger('SearchWhooshMatHang')
    @timer('SearchWhooshMatHang')
    def create_document_ix(self):
        from src.repository.MatHangRepo import MatHangRepo
        mat_hang_repository = MatHangRepo()
        mat_hang_list = mat_hang_repository.list()
        for mat_hang in mat_hang_list:
            self.add_or_update_document_ix(mat_hang.id, mat_hang.ten_hang)

    def delete_document_ix(self, doc_id):
        writer = self.ix_mat_hang.writer()
        writer.delete_by_term('id', doc_id)
        writer.commit()
       
    def add_or_update_document_ix(self, doc_id, ten_mat_hang):
        writer = self.ix_mat_hang.writer()
        writer.update_document(id=doc_id, ten_mat_hang=ten_mat_hang)
        writer.commit()

    @logger('SearchWhooshMatHang')
    @timer('SearchWhooshMatHang')
    def search(self, keyword, field='ten_mat_hang') -> list[dict]:
        with self.ix_mat_hang.searcher() as searcher:
            query = QueryParser(field, self.ix_mat_hang.schema).parse(keyword)
            results = searcher.search(query, limit=500)
            # print(len(results))
            # print(results)
            results_dict = [dict(result) for result in results]
            return results_dict
            
class SearchWhooshKhachHang(SearchWhoosh):
    @logger('SearchWhooshKhachHang')
    @timer('SearchWhooshKhachHang')
    def __init__(self):
        super().__init__()
        self.schema_khach_hang = Schema(
            id=ID(stored=True, unique=True),
            ten_khach_hang=TEXT(stored=True)
        )
        self.ix_khach_hang = None
        self.index_name_khach_hang = "khach_hang"
        self.create_index()
        
    def create_index(self):
        if not os.path.exists(WHOOSH_PATH):
            os.mkdir(WHOOSH_PATH)
        if not exists_in(WHOOSH_PATH, indexname=self.index_name_khach_hang):
            self.ix_khach_hang = create_in(WHOOSH_PATH, self.schema_khach_hang, indexname=self.index_name_khach_hang)
        else:
            self.ix_khach_hang = open_dir(WHOOSH_PATH, indexname=self.index_name_khach_hang)
            
    @logger('SearchWhooshKhachHang')
    @timer('SearchWhooshKhachHang')
    def create_document_ix(self):
        from src.repository.KhachHangRepo import KhachHangRepo
        khach_hang_repository = KhachHangRepo()
        khach_hang_list = khach_hang_repository.list()
        for khach_hang in khach_hang_list:
            self.add_or_update_document_ix(khach_hang.id, khach_hang.ten_khach_hang)
        
    def delete_document_ix(self, doc_id):
        writer = self.ix_khach_hang.writer()
        writer.delete_by_term('id', doc_id)
        writer.commit()
        
    def add_or_update_document_ix(self, doc_id, ten_khach_hang):
        writer = self.ix_khach_hang.writer()
        writer.update_document(id=doc_id, ten_khach_hang=ten_khach_hang)
        writer.commit()

    @logger('SearchWhooshKhachHang')
    @timer('SearchWhooshKhachHang')
    def search(self, keyword, field='ten_khach_hang') -> list[dict]:
        with self.ix_khach_hang.searcher() as searcher:
            query = QueryParser(field, self.ix_khach_hang.schema).parse(keyword)
            results = searcher.search(query, limit=500)
            results_dict = [dict(result) for result in results]
            return results_dict
        
class SearchWhooshNCC(SearchWhoosh):
    @logger('SearchWhooshNCC')
    @timer('SearchWhooshNCC')
    def __init__(self):
        super().__init__()
        self.schema_ncc = Schema(
            id=ID(stored=True, unique=True),
            ten_ncc=TEXT(stored=True)
        )
        self.ix_ncc = None
        self.index_name_ncc = "ncc"
        self.create_index()

    def create_index(self):
        if not os.path.exists(WHOOSH_PATH):
            os.mkdir(WHOOSH_PATH)
        if not exists_in(WHOOSH_PATH, indexname=self.index_name_ncc):
            self.ix_ncc = create_in(WHOOSH_PATH, self.schema_ncc, indexname=self.index_name_ncc)
        else:
            self.ix_ncc = open_dir(WHOOSH_PATH, indexname=self.index_name_ncc)
        
    @logger('SearchWhooshNCC')
    @timer('SearchWhooshNCC')    
    def create_document_ix(self):
        from src.repository.NccRepo import NCCRepo
        ncc_repository = NCCRepo()
        ncc_list = ncc_repository.list()
        for ncc in ncc_list:
            self.add_or_update_document_ix(ncc.id, ncc.ten_ncc)

    def delete_document_ix(self, doc_id):
        writer = self.ix_ncc.writer()
        writer.delete_by_term('id', doc_id)
        writer.commit()

    def add_or_update_document_ix(self, doc_id, ten_ncc):
        writer = self.ix_ncc.writer()
        writer.update_document(id=doc_id, ten_ncc=ten_ncc)
        writer.commit()

    @logger('SearchWhooshNCC')
    @timer('SearchWhooshNCC')
    def search(self, keyword, field='ten_ncc') -> list[dict]:
        with self.ix_ncc.searcher() as searcher:
            query = QueryParser(field, self.ix_ncc.schema).parse(keyword)
            results = searcher.search(query, limit=500)
            results_dict = [dict(result) for result in results]
            return results_dict
          