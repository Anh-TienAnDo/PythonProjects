
from datetime import datetime, timedelta

def format_string_to_date(date_string):
    # Chuyển đổi chuỗi thành đối tượng datetime
    formatted_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Cộng thêm 6 giờ
    date_vie = formatted_date + timedelta(hours=6)
    # Kết quả
    return date_vie