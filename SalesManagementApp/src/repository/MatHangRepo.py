import sqlite3
from contants import MAT_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.MatHangEntity import MatHang
from src.utils.ConvertEntity import ConvertMatHang

class MatHangRepo:
    def __init__(self):
        logging.info('---MatHangRepo initializing---')
        self.db_name = DATABASE_PATH
        self.convert_mat_hang = ConvertMatHang()
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all(self, sort_by: str, limit: str, offset: str) -> list[MatHang]:
        logging.info('Getting all products')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {MAT_HANG_TABLE} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}') 
            data = cursor.fetchall()
            mat_hang_list = self.convert_mat_hang.convert_to_entity_list(data)
            return mat_hang_list
        except Exception as e:
            logging.error('Error getting all products %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
            
    def search(self, sort_by: str, where: str, params: list, limit: str, offset: str) -> list[MatHang]:
        logging.info('Searching products')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {MAT_HANG_TABLE} WHERE {where} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}', params)
            data = cursor.fetchall()
            mat_hang_list = self.convert_mat_hang.convert_to_entity_list(data)
            return mat_hang_list
        except Exception as e:
            logging.error('Error searching products %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def calculate_total(self, where=None, params=None):
        logging.info('Calculating total products')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            if where is None:
                cursor.execute(f'SELECT COUNT(*), SUM(so_luong) FROM {MAT_HANG_TABLE}')
            else:
                cursor.execute(f'SELECT COUNT(*), SUM(so_luong) FROM {MAT_HANG_TABLE} WHERE {where}', params)
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error('Error calculating total products %s', e)
            return (0, 0)
        finally:
            cursor.close()
            connection.close()
        
    def list(self) -> list[MatHang]:
        logging.info('Getting all products')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {MAT_HANG_TABLE}')
            data = cursor.fetchall()
            mat_hang_list = self.convert_mat_hang.convert_to_entity_list(data)
            return mat_hang_list
        except Exception as e:
            logging.error('Error getting all products %s', e)
            return []
        finally:
            cursor.close()
            connection.close()

    def get_by_id(self, mat_hang_id) -> MatHang:
        logging.info('Getting product by id %s', mat_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {MAT_HANG_TABLE} WHERE id = ?', (mat_hang_id,))
            data = cursor.fetchone()
            return MatHang(*data) if data else None
        except Exception as e:
            logging.error('Error getting product by id %s', e)
            return None
        finally:
            cursor.close()
            connection.close()

    def create(self, mat_hang: MatHang) -> bool:
        logging.info('Creating product %s', mat_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'''INSERT INTO {MAT_HANG_TABLE}
                                (id, ten_hang, don_vi, so_luong, gia_le, gia_si, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', mat_hang.to_tuple())
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating product %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
        
    def create_many(self, mat_hang_list) -> bool:
        logging.info('Creating product %s', mat_hang_list)
        connection = self.get_connection()
        cursor = connection.cursor()
        mat_hang_types = [mat_hang.to_tuple() for mat_hang in mat_hang_list]
        try:
            cursor.executemany(f'''INSERT INTO {MAT_HANG_TABLE}
                                (id, ten_hang, don_vi, so_luong, gia_le, gia_si, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', mat_hang_types)
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating product %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def update(self, mat_hang_id, mat_hang: MatHang) -> bool:
        logging.info('Updating product %s', mat_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        ten_hang = mat_hang.ten_hang
        don_vi = mat_hang.don_vi
        so_luong = mat_hang.so_luong
        gia_le = mat_hang.gia_le
        gia_si = mat_hang.gia_si
        is_active = mat_hang.is_active
        try:
            cursor.execute(f'UPDATE {MAT_HANG_TABLE} SET ten_hang = ?, don_vi = ?, so_luong = ?, gia_le = ?, gia_si = ?, is_active = ? WHERE id = ?', (
                ten_hang, don_vi, so_luong, gia_le, gia_si, is_active, mat_hang_id))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating product %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
        
    def update_so_luong(self, mat_hang_id, so_luong) -> bool:
        logging.info('Updating so luong mat hang %s', so_luong)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'UPDATE {MAT_HANG_TABLE} SET so_luong = ? WHERE id = ?', (
                so_luong, mat_hang_id))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating so luong mat hang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def delete(self, mat_hang_id) -> bool:
        logging.info('Deleting product by id %s', mat_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'DELETE FROM {MAT_HANG_TABLE} WHERE id = ?', (mat_hang_id,))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting product %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
            
    def check_exist_id(self, mat_hang_id) -> bool:
        logging.info('Checking product exist by id %s', mat_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {MAT_HANG_TABLE} WHERE id = ?', (mat_hang_id,))
            data = cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking product exist %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    # def __del__(self):
    #     logging.info('Closing database connection to mathang')
    #     if cursor:
    #         cursor.close()
    #     if self.connection:
    #         self.connection.close()
            
    
        
    
