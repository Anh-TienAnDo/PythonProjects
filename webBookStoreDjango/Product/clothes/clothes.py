from .models import Clothes
from fuzzywuzzy import fuzz

def search_clothes(query):
    # Lấy toàn bộ quần áo từ cơ sở dữ liệu
    all_clothes = Clothes.objects.all()

    # Khởi tạo danh sách kết quả
    result = []

    # Lặp qua từng sản phẩm quần áo
    for clothes in all_clothes:
        # So sánh tên quần áo với query
        name_similarity = fuzz.partial_ratio(query, clothes.name.lower())

        # So sánh tên nhà sản xuất với query
        producer_similarity = fuzz.partial_ratio(query, clothes.producer_id.name.lower()) if clothes.producer_id else 0

        # So sánh tên loại quần áo với query
        type_similarity = fuzz.partial_ratio(query, clothes.type_id.name.lower()) if clothes.type_id else 0

        # Kiểm tra xem tỷ lệ tương đồng của từng thuộc tính có lớn hơn 70 không
        if name_similarity >= 70 or producer_similarity >= 70 or type_similarity >= 70:
            result.append(clothes)

    return result
