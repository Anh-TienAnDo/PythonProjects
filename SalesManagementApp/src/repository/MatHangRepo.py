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

    def get_all(self):
        logging.info('Getting all products')
        try:
            self.cursor.execute(f'SELECT * FROM {MAT_HANG_TABLE}')
            data = self.cursor.fetchall()
            mat_hang_list = [MatHang(*row) for row in data]
            return mat_hang_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all products %s', e)
            return None
        finally:
            self.cursor.close()
            logging.info('Closed cursor')

    def get_by_id(self, id):
        logging.info('Getting product by id %s', id)
        try:
            self.cursor.execute(f'SELECT * FROM {MAT_HANG_TABLE} WHERE id = ?', (id,))
            data = self.cursor.fetchone()
            return MatHang(*data) if data else None
        except sqlite3.IntegrityError as e:
            logging.error('Error getting product by id %s', e)
            return None
        finally:
            self.cursor.close()
            logging.info('Closed cursor')

    def create(self, mat_hang):
        logging.info('Creating product %s', mat_hang)
        try:
            self.cursor.execute(f'''INSERT INTO {MAT_HANG_TABLE}
                                (id, ten_hang, don_vi, so_luong, gia_le, gia_si, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', mat_hang)
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error creating product %s', e)
            return False
        finally:
            self.cursor.close()
            logging.info('Closed cursor')

    def update(self, id, mat_hang):
        logging.info('Updating product %s', mat_hang)
        try:
            self.cursor.execute(f'UPDATE {MAT_HANG_TABLE} SET ten_hang = ?, don_vi = ?, so_luong = ?, gia_le = ?, gia_si = ?, is_active = ? WHERE id = ?', (*mat_hang, id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error updating product %s', e)
            return False
        finally:
            self.cursor.close()
            logging.info('Closed cursor')

    def delete(self, id):
        logging.info('Deleting product by id %s', id)
        try:
            self.cursor.execute(f'DELETE FROM {MAT_HANG_TABLE} WHERE id = ?', (id,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error deleting product %s', e)
            return False
        finally:
            self.cursor.close()
            logging.info('Closed cursor')
    
    def __del__(self):
        logging.info('---MatHangRepo closing---')
        self.connection.close()
        logging.info('Closed database connection %s', DATABASE_PATH)

