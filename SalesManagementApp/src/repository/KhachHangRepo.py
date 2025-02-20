import sqlite3
from contants import KHACH_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.KhachHangEntity import KhachHang
from src.utils.ConvertEntity import ConvertKhachHang

class KhachHangRepo:
    def __init__(self):
        logging.info('---KhachHangRepo initializing---')
        self.db_name = DATABASE_PATH
        self.convert_khach_hang = ConvertKhachHang()
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all(self, sort_by: str, limit: str, offset: str) -> list[KhachHang]:
        logging.info('Getting all khach hang')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {KHACH_HANG_TABLE} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}')
            data = cursor.fetchall()
            khach_hang_list = self.convert_khach_hang.convert_to_entity_list(data)
            return khach_hang_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def search(self, sort_by: str, where: str, params: list, limit: str, offset: str) -> list[KhachHang]:
        logging.info('Searching khachhang')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {KHACH_HANG_TABLE} WHERE {where} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}', params)
            data = cursor.fetchall()
            khach_hang_list = self.convert_khach_hang.convert_to_entity_list(data)
            return khach_hang_list
        except Exception as e:
            logging.error('Error searching khachhang %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def calculate_total(self, where=None, params=None):
        logging.info('Calculating total khachhang')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            if where is None:
                cursor.execute(f'SELECT COUNT(*) FROM {KHACH_HANG_TABLE}')
            else:
                cursor.execute(f'SELECT COUNT(*) FROM {KHACH_HANG_TABLE} WHERE {where}', params)
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error('Error calculating total khachhang %s', e)
            return (0,)
        finally:
            cursor.close()
            connection.close()
        
    def list(self) -> list[KhachHang]:
        logging.info('Getting all khach hang')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {KHACH_HANG_TABLE}')
            data = cursor.fetchall()
            khach_hang_list = self.convert_khach_hang.convert_to_entity_list(data)
            return khach_hang_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()

    def get_by_id(self, khach_hang_id) -> KhachHang:
        logging.info('Getting khachhang by id %s', khach_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {KHACH_HANG_TABLE} WHERE id = ?', (khach_hang_id,))
            data = cursor.fetchone()
            return KhachHang(*data) if data else None
        except Exception as e:
            logging.error('Error getting khachhang by id %s', e)
            return None
        finally:
            cursor.close()
            connection.close()

    def create(self, khach_hang: KhachHang) -> bool:
        logging.info('Creating khachhang %s', khach_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'''INSERT INTO {KHACH_HANG_TABLE}
                                (id, ten_khach_hang, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', khach_hang.to_tuple())
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating khachhang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
        
    def create_many(self, khach_hang_list) -> bool:
        logging.info('Creating khachhang %s', khach_hang_list)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.executemany(f'''INSERT INTO {KHACH_HANG_TABLE}
                                (id, ten_khach_hang, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', [khach_hang.to_tuple() for khach_hang in khach_hang_list])
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating khachhang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def update(self, khach_hang_id, khach_hang: KhachHang) -> bool:
        logging.info('Updating khachhang %s', khach_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        ten_khach_hang = khach_hang.ten_khach_hang
        dien_thoai = khach_hang.dien_thoai
        email = khach_hang.email
        dia_chi = khach_hang.dia_chi
        ghi_chu = khach_hang.ghi_chu
        is_active = khach_hang.is_active
        try:
            cursor.execute(f'UPDATE {KHACH_HANG_TABLE} SET ten_khach_hang = ?, dien_thoai = ?, email = ?, dia_chi = ?, ghi_chu = ?, is_active = ? WHERE id = ?', (
                ten_khach_hang, dien_thoai, email, dia_chi, ghi_chu, is_active, khach_hang_id))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating khachhang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def delete(self, khach_hang_id) -> bool:
        logging.info('Deleting khachhang by id %s', khach_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'DELETE FROM {KHACH_HANG_TABLE} WHERE id = ?', (khach_hang_id,))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting khachhang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
            
    def check_exist_id(self, khach_hang_id) -> bool:
        logging.info('Checking khachhang exist by id %s', khach_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {KHACH_HANG_TABLE} WHERE id = ?', (khach_hang_id,))
            data = cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking khachhang exist %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    # def __del__(self):
    #     logging.info('Closing database connection to khachhang')
    #     if cursor:
    #         cursor.close()
    #     if self.connection:
    #         self.connection.close()
        
    
