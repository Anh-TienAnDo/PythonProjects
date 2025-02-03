import sqlite3
from contants import BAN_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.BanHangEntity import BanHang


class BanHangRepo:
    def __init__(self):
        logging.info('---BanHangRepo initializing---')
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.info('Connected to database %s', DATABASE_PATH)

    def get_all(self, sort_by: str, where: str) -> list[BanHang]:
        logging.info('Getting all banhang')
        try:
            self.cursor.execute(f'SELECT * FROM {BAN_HANG_TABLE} WHERE {where} ORDER BY {sort_by}')
            data = self.cursor.fetchall()
            ban_hang_list = [BanHang(*row) for row in data]
            return ban_hang_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all %s', e)
            return None
        
    def list(self) -> list[BanHang]:
        logging.info('Getting all banhang')
        try:
            self.cursor.execute(f'SELECT * FROM {BAN_HANG_TABLE}')
            data = self.cursor.fetchall()
            ban_hang_list = [BanHang(*row) for row in data]
            return ban_hang_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all %s', e)
            
    def report(self, sort_by: str, where: str) -> list:
        self.cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien) FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY id_mat_hang ORDER BY {sort_by}')
        data = self.cursor.fetchall()
        return data
    
    def report_detail_mat_hang(self, sort_by: str, where: str) -> list:
        # where: ngay_ban = '2021-09-01', id_mat_hang = 'MH0001'
        self.cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien), ngay_ban FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY ngay_ban ORDER BY {sort_by}')
        data = self.cursor.fetchall()
        return data
    
    def report_loi_nhuan(self, where: str) -> list:
        self.cursor.execute(f'SELECT sum(thanh_tien), ngay_ban FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY ngay_ban')
        data = self.cursor.fetchall()
        return data

    def get_by_id(self, ban_hang_id) -> BanHang:
        logging.info('Getting banhang by id %s', ban_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {BAN_HANG_TABLE} WHERE id = ?', (ban_hang_id,))
            data = self.cursor.fetchone()
            return BanHang(*data) if data else None
        except sqlite3.IntegrityError as e:
            logging.error('Error getting banhang by id %s', e)
            return None

    def create(self, ban_hang: BanHang) -> bool:
        logging.info('Creating banhang %s', ban_hang)
        try:
            self.cursor.execute(f'''INSERT INTO {BAN_HANG_TABLE}
                                (id, id_mat_hang, ten_hang, don_vi, so_luong, gia_ban, khach_hang, thanh_tien, ghi_chu, ngay_ban) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ban_hang.to_tuple())
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error creating banhang %s', e)
            return False

    def update(self, ban_hang_id, ban_hang: BanHang) -> bool:
        logging.info('Updating banhang %s', ban_hang)
        ten_hang = ban_hang.ten_hang
        don_vi = ban_hang.don_vi
        so_luong = ban_hang.so_luong
        gia_ban = ban_hang.gia_ban
        khach_hang = ban_hang.khach_hang
        thanh_tien = ban_hang.thanh_tien
        ghi_chu = ban_hang.ghi_chu
        try:
            self.cursor.execute(f'UPDATE {BAN_HANG_TABLE} SET ten_hang = ?, don_vi = ?, so_luong = ?, gia_ban = ?, khach_hang = ?, thanh_tien = ?, ghi_chu = ? WHERE id = ?', (
                ten_hang, don_vi, so_luong, gia_ban, khach_hang, thanh_tien, ghi_chu, ban_hang_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error updating banhang %s', e)
            return False

    def delete(self, ban_hang_id) -> bool:
        logging.info('Deleting banhang by id %s', ban_hang_id)
        try:
            self.cursor.execute(
                f'DELETE FROM {BAN_HANG_TABLE} WHERE id = ?', (ban_hang_id,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error deleting banhang %s', e)
            return False
            
    def check_exist_id(self, ban_hang_id) -> bool:
        logging.info('Checking banhang exist by id %s', ban_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {BAN_HANG_TABLE} WHERE id = ?', (ban_hang_id,))
            data = self.cursor.fetchone()
            return True if data else False
        except sqlite3.IntegrityError as e:
            logging.error('Error checking banhang exist %s', e)
            return False

    def __del__(self):
        logging.info('Closing database connection')
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    
