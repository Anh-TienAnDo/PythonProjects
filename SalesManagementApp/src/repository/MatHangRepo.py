import sqlite3
from contants import MAT_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.MatHangEntity import MatHang


class MatHangRepo:
    def __init__(self):
        logging.info('---MatHangRepo initializing---')
        logging.info('Connecting to database %s', DATABASE_PATH)
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.info('Connected to database %s', DATABASE_PATH)

    def get_all(self, sort_by: str) -> list[MatHang]:
        logging.info('Getting all products')
        try:
            self.cursor.execute(f'SELECT * FROM {MAT_HANG_TABLE} ORDER BY {sort_by}')
            data = self.cursor.fetchall()
            mat_hang_list = [MatHang(*row) for row in data]
            return mat_hang_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all products %s', e)
            return None

    def get_by_id(self, mat_hang_id) -> MatHang:
        logging.info('Getting product by id %s', mat_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {MAT_HANG_TABLE} WHERE id = ?', (mat_hang_id,))
            data = self.cursor.fetchone()
            return MatHang(*data) if data else None
        except sqlite3.IntegrityError as e:
            logging.error('Error getting product by id %s', e)
            return None

    def create(self, mat_hang: MatHang) -> bool:
        logging.info('Creating product %s', mat_hang)
        try:
            self.cursor.execute(f'''INSERT INTO {MAT_HANG_TABLE}
                                (id, ten_hang, don_vi, so_luong, gia_le, gia_si, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', mat_hang.to_tuple())
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error creating product %s', e)
            return False

    def update(self, mat_hang_id, mat_hang: MatHang) -> bool:
        logging.info('Updating product %s', mat_hang)
        ten_hang = mat_hang.ten_hang
        don_vi = mat_hang.don_vi
        so_luong = mat_hang.so_luong
        gia_le = mat_hang.gia_le
        gia_si = mat_hang.gia_si
        is_active = mat_hang.is_active
        try:
            self.cursor.execute(f'UPDATE {MAT_HANG_TABLE} SET ten_hang = ?, don_vi = ?, so_luong = ?, gia_le = ?, gia_si = ?, is_active = ? WHERE id = ?', (
                ten_hang, don_vi, so_luong, gia_le, gia_si, is_active, mat_hang_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error updating product %s', e)
            return False

    def delete(self, mat_hang_id) -> bool:
        logging.info('Deleting product by id %s', mat_hang_id)
        try:
            self.cursor.execute(
                f'DELETE FROM {MAT_HANG_TABLE} WHERE id = ?', (mat_hang_id,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error deleting product %s', e)
            return False
            
    def check_exist_id(self, mat_hang_id) -> bool:
        logging.info('Checking product exist by id %s', mat_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {MAT_HANG_TABLE} WHERE id = ?', (mat_hang_id,))
            data = self.cursor.fetchone()
            return True if data else False
        except sqlite3.IntegrityError as e:
            logging.error('Error checking product exist %s', e)
            return False

    def __del__(self):
        logging.info('Closing database connection')
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    
