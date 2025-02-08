import sqlite3
from contants import KHACH_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.KhachHangEntity import KhachHang


class KhachHangRepo:
    def __init__(self):
        logging.info('---KhachHangRepo initializing---')
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.info('Connected to database %s', DATABASE_PATH)

    def get_all(self, sort_by: str, limit: str, offset: str) -> list[KhachHang]:
        logging.info('Getting all khach hang')
        try:
            self.cursor.execute(f'SELECT * FROM {KHACH_HANG_TABLE} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}')
            data = self.cursor.fetchall()
            khach_hang_list = [KhachHang(*row) for row in data]
            return khach_hang_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        
    def search(self, sort_by: str, where: str, params: list, limit: str, offset: str) -> list[KhachHang]:
        logging.info('Searching khachhang')
        try:
            self.cursor.execute(f'SELECT * FROM {KHACH_HANG_TABLE} WHERE {where} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}', params)
            data = self.cursor.fetchall()
            khach_hang_list = [KhachHang(*row) for row in data]
            return khach_hang_list
        except Exception as e:
            logging.error('Error searching khachhang %s', e)
            return []
        
    def calculate_total(self, where=None, params=None):
        logging.info('Calculating total khachhang')
        try:
            if where is None:
                self.cursor.execute(f'SELECT COUNT(*) FROM {KHACH_HANG_TABLE}')
            else:
                self.cursor.execute(f'SELECT COUNT(*) FROM {KHACH_HANG_TABLE} WHERE {where}', params)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            logging.error('Error calculating total khachhang %s', e)
            return None
        
    def list(self) -> list[KhachHang]:
        logging.info('Getting all khach hang')
        try:
            self.cursor.execute(f'SELECT * FROM {KHACH_HANG_TABLE}')
            data = self.cursor.fetchall()
            khach_hang_list = [KhachHang(*row) for row in data]
            return khach_hang_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []

    def get_by_id(self, khach_hang_id) -> KhachHang:
        logging.info('Getting khachhang by id %s', khach_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {KHACH_HANG_TABLE} WHERE id = ?', (khach_hang_id,))
            data = self.cursor.fetchone()
            return KhachHang(*data) if data else None
        except Exception as e:
            logging.error('Error getting khachhang by id %s', e)
            return None

    def create(self, khach_hang: KhachHang) -> bool:
        logging.info('Creating khachhang %s', khach_hang)
        try:
            self.cursor.execute(f'''INSERT INTO {KHACH_HANG_TABLE}
                                (id, ten_khach_hang, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', khach_hang.to_tuple())
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating khachhang %s', e)
            return False
        
    def create_many(self, khach_hang_list) -> bool:
        logging.info('Creating khachhang %s', khach_hang_list)
        try:
            self.cursor.executemany(f'''INSERT INTO {KHACH_HANG_TABLE}
                                (id, ten_khach_hang, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', [khach_hang.to_tuple() for khach_hang in khach_hang_list])
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating khachhang %s', e)
            return False

    def update(self, khach_hang_id, khach_hang: KhachHang) -> bool:
        logging.info('Updating khachhang %s', khach_hang)
        ten_khach_hang = khach_hang.ten_khach_hang
        dien_thoai = khach_hang.dien_thoai
        email = khach_hang.email
        dia_chi = khach_hang.dia_chi
        ghi_chu = khach_hang.ghi_chu
        is_active = khach_hang.is_active
        try:
            self.cursor.execute(f'UPDATE {KHACH_HANG_TABLE} SET ten_khach_hang = ?, dien_thoai = ?, email = ?, dia_chi = ?, ghi_chu = ?, is_active = ? WHERE id = ?', (
                ten_khach_hang, dien_thoai, email, dia_chi, ghi_chu, is_active, khach_hang_id))
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating khachhang %s', e)
            return False

    def delete(self, khach_hang_id) -> bool:
        logging.info('Deleting khachhang by id %s', khach_hang_id)
        try:
            self.cursor.execute(
                f'DELETE FROM {KHACH_HANG_TABLE} WHERE id = ?', (khach_hang_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting khachhang %s', e)
            return False
            
    def check_exist_id(self, khach_hang_id) -> bool:
        logging.info('Checking khachhang exist by id %s', khach_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {KHACH_HANG_TABLE} WHERE id = ?', (khach_hang_id,))
            data = self.cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking khachhang exist %s', e)
            return False

    def __del__(self):
        logging.info('Closing database connection')
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    
