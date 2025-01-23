import sqlite3
from contants import DATABASE_PATH, BAN_HANG_TABLE
class BanHangRepo:
    def __init__(self):
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
    def report_by_month(self, month: str, year: str) -> list:
        where = "strftime('%m-%Y', ngay_ban) = '01-2025'"
        self.cursor.execute(f'SELECT count(id), sum(so_luong), sum(thanh_tien), ten_hang, ngay_ban FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY id_mat_hang ORDER BY sum(so_luong)')
        data = self.cursor.fetchall()
        return data
    
    def report_by_day(self, day: str, month: str, year: str) -> list:
        where = "strftime('%d-%m-%Y', ngay_ban) = '22-01-2025'"
        self.cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id) as so_lan_ban, sum(so_luong) as tong_so_luong, sum(thanh_tien) as tong_tien, ngay_ban FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY id_mat_hang ORDER BY ngay_ban')
        data = self.cursor.fetchall()
        return data
    
ban_hang = BanHangRepo()
data = ban_hang.report_by_month('01', '2025')
print(data)