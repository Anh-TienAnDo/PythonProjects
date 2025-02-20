import sqlite3
from contants import NCC_TABLE, DATABASE_PATH
import logging
from src.entity.NccEntity import NCC
from src.utils.ConvertEntity import ConvertNCC

class NCCRepo:
    def __init__(self):
        logging.info('---NCCRepo initializing---')
        self.db_name = DATABASE_PATH
        self.convert_ncc = ConvertNCC()
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all(self, sort_by: str, limit: str, offset: str) -> list[NCC]:
        logging.info('Getting all ncc')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {NCC_TABLE} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}')
            data = cursor.fetchall()
            ncc_list = self.convert_ncc.convert_to_entity_list(data)
            return ncc_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def search(self, sort_by: str, where: str, params: list, limit: str, offset: str) -> list[NCC]:
        logging.info('Searching ncc')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {NCC_TABLE} WHERE {where} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}', params)
            data = cursor.fetchall()
            ncc_list = self.convert_ncc.convert_to_entity_list(data)
            return ncc_list
        except Exception as e:
            logging.error('Error searching ncc %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def calculate_total(self, where=None, params=None):
        logging.info('Calculating total ncc')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            if where is None:
                cursor.execute(f'SELECT COUNT(*) FROM {NCC_TABLE}')
            else:
                cursor.execute(f'SELECT COUNT(*) FROM {NCC_TABLE} WHERE {where}', params)
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error('Error calculating total ncc %s', e)
            return (0,)
        finally:
            cursor.close()
            connection.close()
        
    def list(self) -> list[NCC]:
        logging.info('Getting all ncc')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {NCC_TABLE}')
            data = cursor.fetchall()
            ncc_list = self.convert_ncc.convert_to_entity_list(data)
            return ncc_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()

    def get_by_id(self, ncc_id) -> NCC:
        logging.info('Getting ncc by id %s', ncc_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {NCC_TABLE} WHERE id = ?', (ncc_id,))
            data = cursor.fetchone()
            return NCC(*data) if data else None
        except Exception as e:
            logging.error('Error getting ncc by id %s', e)
            return None
        finally:
            cursor.close()
            connection.close()

    def create(self, ncc: NCC) -> bool:
        logging.info('Creating ncc %s', ncc)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'''INSERT INTO {NCC_TABLE}
                                (id, ten_ncc, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', ncc.to_tuple())
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating ncc %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
        
    def create_many(self, ncc_list) -> bool:
        logging.info('Creating ncc %s', ncc_list)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.executemany(f'''INSERT INTO {NCC_TABLE}
                                (id, ten_ncc, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', [ncc.to_tuple() for ncc in ncc_list])
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating ncc %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def update(self, ncc_id, ncc: NCC) -> bool:
        logging.info('Updating ncc %s', ncc)
        connection = self.get_connection()
        cursor = connection.cursor()
        ten_ncc = ncc.ten_ncc
        dien_thoai = ncc.dien_thoai
        email = ncc.email
        dia_chi = ncc.dia_chi
        ghi_chu = ncc.ghi_chu
        is_active = ncc.is_active
        try:
            cursor.execute(f'UPDATE {NCC_TABLE} SET ten_ncc = ?, dien_thoai = ?, email = ?, dia_chi = ?, ghi_chu = ?, is_active = ? WHERE id = ?', (
                ten_ncc, dien_thoai, email, dia_chi, ghi_chu, is_active, ncc_id))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating ncc %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def delete(self, ncc_id) -> bool:
        logging.info('Deleting ncc by id %s', ncc_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'DELETE FROM {NCC_TABLE} WHERE id = ?', (ncc_id,))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting ncc %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
            
    def check_exist_id(self, ncc_id) -> bool:
        logging.info('Checking ncc exist by id %s', ncc_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {NCC_TABLE} WHERE id = ?', (ncc_id,))
            data = cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking ncc exist %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    # def __del__(self):
    #     logging.info('Closing database connection to ncc')
    #     if cursor:
    #         cursor.close()
    #     if self.connection:
    #         self.connection.close()
        
    
