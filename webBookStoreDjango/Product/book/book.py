from fuzzywuzzy import fuzz
from .models import *

def search_books(query):
    # Lấy toàn bộ sách từ cơ sở dữ liệu
    all_books = Book.objects.all()
    # Khởi tạo danh sách kết quả
    result = []
    # Lặp qua từng cuốn sách
    for book in all_books:
        # So sánh tên sách với query
        name_similarity = fuzz.partial_ratio(query, book.name.lower())
        # So sánh tác giả của sách với query
        author_similarity = fuzz.partial_ratio(query, book.author.name.lower()) if book.author else 0
        # So sánh danh mục của sách với query
        categories_similarity = max([fuzz.partial_ratio(query, category.name.lower()) for category in book.categories.all()])
        # So sánh nhà xuất bản của sách với query
        publisher_similarity = fuzz.partial_ratio(query, book.publisher.name.lower()) if book.publisher else 0
        # Kiểm tra xem tỷ lệ tương đồng của từng thuộc tính có lớn hơn 70 không
        if name_similarity >= 70 or author_similarity >= 70 or categories_similarity >= 70 or publisher_similarity >= 70:
            result.append(book)
    return result