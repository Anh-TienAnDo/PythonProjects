from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from contants import WHOOSH_INDEX_DIR, WHOOSH_PATH, MAT_HANG_SORT_OPTIONS
import os
import logging

class SearchWhoosh:
    def __init__(self):
        self.schema_mat_hang = Schema(
            id=ID(stored=True, unique=True),
            ten_mat_hang=TEXT(stored=True)
        )
        self.index_dir = WHOOSH_INDEX_DIR
    
    
        
class SearchWhooshMatHang(SearchWhoosh):
    def __init__(self):
        super().__init__()
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

    def search(self, keyword, field='ten_mat_hang') -> list[dict]:
        with self.ix_mat_hang.searcher() as searcher:
            query = QueryParser(field, self.ix_mat_hang.schema).parse(keyword)
            results = searcher.search(query)
            results_dict = [dict(result) for result in results]
            return results_dict
            
          