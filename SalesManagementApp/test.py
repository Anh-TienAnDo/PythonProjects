# delete 
# gen id
# view add product
# get all + sort
# nháy chuột và copy

from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.query import Prefix
import os
from contants import CURRENT_WORKING_DIRECTORY, WHOOSH_INDEX_DIR, WHOOSH_PATH

# Định nghĩa schema cho mặt hàng
schema_mat_hang = Schema(
    id=ID(stored=True, unique=True),
    ten_mat_hang=TEXT(stored=True)
)

# Tạo thư mục để lưu trữ chỉ mục
index_dir = WHOOSH_INDEX_DIR
# if not os.path.exists(os.path.join(CURRENT_WORKING_DIRECTORY, index_dir)):
#     os.mkdir(os.path.join(CURRENT_WORKING_DIRECTORY, index_dir))
# # Kiểm tra xem chỉ mục đã tồn tại hay chưa
ix_mat_hang = open_dir(WHOOSH_PATH, indexname="mat_hang")
# else:
#     ix_mat_hang = create_in(WHOOSH_PATH, schema_mat_hang, indexname="mat_hang")


# Cập nhật dữ liệu trong chỉ mục mặt hàng
def add_or_update_document(ix, doc_id, doc):
    writer = ix.writer()
    writer.update_document(id=doc_id, **doc)
    writer.commit()

# Xóa dữ liệu khỏi chỉ mục mặt hàng
def delete_document(ix, doc_id):
    writer = ix.writer()
    writer.delete_by_term('id', doc_id)
    writer.commit()

# Hàm thực hiện tìm kiếm
def search(query_str, index):
    with index.searcher() as searcher:
        query = QueryParser("ten_mat_hang", index.schema).parse(query_str)
        results = searcher.search(query)
        results = [dict(result) for result in results]
        for result in results:
            print(result)
            
def search_prefix(prefix_str, index):
    with index.searcher() as searcher:
        query = Prefix("ten_mat_hang", prefix_str)
        results = searcher.search(query)
        for result in results:
            print(result)

# Cập nhật tài liệu
# add_or_update_document(ix_mat_hang, "1", {"ten_mat_hang": "Sản phẩm 2"})

# # Xóa tài liệu
# delete_document(ix_mat_hang, "1")

# Tìm kiếm tài liệu
print("Tìm kiếm theo tên mặt hàng:")
search("", ix_mat_hang) # check viết hoa, dấu cách, dấu chấm
