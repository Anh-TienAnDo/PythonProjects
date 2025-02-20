import sqlite3
from contants import NHAP_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.NhapHangEntity import NhapHang
from src.utils.ConvertEntity import ConvertNhapHang

class NhapHangRepo:
    def __init__(self):
        logging.info('---NhapHangRepo initializing---')
        self.db_name = DATABASE_PATH
        self.convert_nhap_hang = ConvertNhapHang()
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all(self, sort_by: str, where: str, limit: str, offset: str) -> list[NhapHang]:
        logging.info('Getting all nhaphang')
        logging.info('SELECT * FROM %s WHERE %s ORDER BY %s LIMIT %s OFFSET %s', NHAP_HANG_TABLE, where, sort_by, limit, offset)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {NHAP_HANG_TABLE} WHERE {where} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}')
            data = cursor.fetchall()
            nhap_hang_list = self.convert_nhap_hang.convert_to_entity_list(data)
            return nhap_hang_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def calculate_total(self, where: str):
        logging.info('Calculating total nhap hang')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT COUNT(*), SUM(so_luong), SUM(thanh_tien) FROM {NHAP_HANG_TABLE} WHERE {where}')
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error('Error calculating total %s', e)
            return (0, 0, 0)
        finally:
            cursor.close()
            connection.close()
        
    def list(self) -> list[NhapHang]:
        logging.info('Getting all nhaphang')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {NHAP_HANG_TABLE}')
            data = cursor.fetchall()
            nhap_hang_list = self.convert_nhap_hang.convert_to_entity_list(data)
            return nhap_hang_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
            
    def report(self, sort_by: str, where: str) -> list:
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien) FROM {NHAP_HANG_TABLE} WHERE {where} GROUP BY id_mat_hang ORDER BY {sort_by}')
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
    
    def report_detail_nhap_hang(self, sort_by: str, where: str) -> list:
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien), ngay_nhap FROM {NHAP_HANG_TABLE} WHERE {where} GROUP BY ngay_nhap ORDER BY {sort_by}')
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
    
    def report_loi_nhuan(self, where: str) -> list:
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT sum(thanh_tien), ngay_nhap FROM {NHAP_HANG_TABLE} WHERE {where} GROUP BY ngay_nhap')
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error('Error getting report loi nhuan %s', e)
            return []
        finally:
            cursor.close()
            connection.close()

    def get_by_id(self, nhap_hang_id) -> NhapHang:
        logging.info('Getting nhaphang by id %s', nhap_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {NHAP_HANG_TABLE} WHERE id = ?', (nhap_hang_id,))
            data = cursor.fetchone()
            return NhapHang(*data) if data else None
        except Exception as e:
            logging.error('Error getting nhaphang by id %s', e)
            return None
        finally:
            cursor.close()
            connection.close()

    def create(self, nhap_hang: NhapHang) -> bool:
        logging.info('Creating nhaphang %s', nhap_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'''INSERT INTO {NHAP_HANG_TABLE}
                                (id, id_mat_hang, ten_hang, don_vi, so_luong, gia_nhap, nha_cung_cap, thanh_tien, ghi_chu, ngay_nhap) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', nhap_hang.to_tuple())
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating nhaphang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
        
    def create_many(self, nhap_hang_list) -> bool:
        logging.info('Creating multiple nhaphang records')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            nhap_hang_tuples = [nhap_hang.to_tuple() for nhap_hang in nhap_hang_list]
            cursor.executemany(f'''INSERT INTO {NHAP_HANG_TABLE}
                                (id, id_mat_hang, ten_hang, don_vi, so_luong, gia_nhap, nha_cung_cap, thanh_tien, ghi_chu, ngay_nhap) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', nhap_hang_tuples)
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating multiple banhang records %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def update(self, nhap_hang_id, nhap_hang: NhapHang) -> bool:
        logging.info('Updating nhaphang %s', nhap_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        ten_hang = nhap_hang.ten_hang
        don_vi = nhap_hang.don_vi
        so_luong = nhap_hang.so_luong
        gia_nhap = nhap_hang.gia_nhap
        nha_cung_cap = nhap_hang.nha_cung_cap
        thanh_tien = nhap_hang.thanh_tien
        ghi_chu = nhap_hang.ghi_chu
        try:
            cursor.execute(f'UPDATE {NHAP_HANG_TABLE} SET ten_hang = ?, don_vi = ?, so_luong = ?, gia_nhap = ?, nha_cung_cap = ?, thanh_tien = ?, ghi_chu = ? WHERE id = ?', (
                ten_hang, don_vi, so_luong, gia_nhap, nha_cung_cap, thanh_tien, ghi_chu, nhap_hang_id))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating nhaphang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def delete(self, nhap_hang_id) -> bool:
        logging.info('Deleting nhaphang by id %s', nhap_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'DELETE FROM {NHAP_HANG_TABLE} WHERE id = ?', (nhap_hang_id,))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting nhaphang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
            
    def check_exist_id(self, nhap_hang_id) -> bool:
        logging.info('Checking nhaphang exist by id %s', nhap_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {NHAP_HANG_TABLE} WHERE id = ?', (nhap_hang_id,))
            data = cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking nhaphang exist %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    # def __del__(self):
    #     logging.info('Closing database connection to nhaphang')
    #     if cursor:
    #         cursor.close()
    #     if self.connection:
    #         self.connection.close()
        
    
