import sqlite3
from contants import NCC_TABLE, DATABASE_PATH
import logging
from src.entity.NccEntity import NCC


class NCCRepo:
    def __init__(self):
        logging.info('---NCCRepo initializing---')
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.info('Connected to database %s', DATABASE_PATH)

    def get_all(self, sort_by: str) -> list[NCC]:
        logging.info('Getting all ncc')
        try:
            self.cursor.execute(f'SELECT * FROM {NCC_TABLE} ORDER BY {sort_by}')
            data = self.cursor.fetchall()
            ncc_list = [NCC(*row) for row in data]
            return ncc_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return None
        
    def search(self, sort_by: str, where: str, params: list) -> list[NCC]:
        logging.info('Searching ncc')
        try:
            self.cursor.execute(f'SELECT * FROM {NCC_TABLE} WHERE {where} ORDER BY {sort_by}', params)
            data = self.cursor.fetchall()
            ncc_list = [NCC(*row) for row in data]
            return ncc_list
        except Exception as e:
            logging.error('Error searching ncc %s', e)
            return None
        
    def list(self) -> list[NCC]:
        logging.info('Getting all ncc')
        try:
            self.cursor.execute(f'SELECT * FROM {NCC_TABLE}')
            data = self.cursor.fetchall()
            ncc_list = [NCC(*row) for row in data]
            return ncc_list
        except Exception as e:
            logging.error('Error getting all %s', e)

    def get_by_id(self, ncc_id) -> NCC:
        logging.info('Getting ncc by id %s', ncc_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {NCC_TABLE} WHERE id = ?', (ncc_id,))
            data = self.cursor.fetchone()
            return NCC(*data) if data else None
        except Exception as e:
            logging.error('Error getting ncc by id %s', e)
            return None

    def create(self, ncc: NCC) -> bool:
        logging.info('Creating ncc %s', ncc)
        try:
            self.cursor.execute(f'''INSERT INTO {NCC_TABLE}
                                (id, ten_ncc, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', ncc.to_tuple())
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating ncc %s', e)
            return False
        
    def create_many(self, ncc_list) -> bool:
        logging.info('Creating ncc %s', ncc_list)
        try:
            self.cursor.executemany(f'''INSERT INTO {NCC_TABLE}
                                (id, ten_ncc, dien_thoai, email, dia_chi, ghi_chu, ngay_tao, is_active) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', [ncc.to_tuple() for ncc in ncc_list])
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating ncc %s', e)
            return False

    def update(self, ncc_id, ncc: NCC) -> bool:
        logging.info('Updating ncc %s', ncc)
        ten_ncc = ncc.ten_ncc
        dien_thoai = ncc.dien_thoai
        email = ncc.email
        dia_chi = ncc.dia_chi
        ghi_chu = ncc.ghi_chu
        is_active = ncc.is_active
        try:
            self.cursor.execute(f'UPDATE {NCC_TABLE} SET ten_ncc = ?, dien_thoai = ?, email = ?, dia_chi = ?, ghi_chu = ?, is_active = ? WHERE id = ?', (
                ten_ncc, dien_thoai, email, dia_chi, ghi_chu, is_active, ncc_id))
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating ncc %s', e)
            return False

    def delete(self, ncc_id) -> bool:
        logging.info('Deleting ncc by id %s', ncc_id)
        try:
            self.cursor.execute(
                f'DELETE FROM {NCC_TABLE} WHERE id = ?', (ncc_id,))
            self.connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting ncc %s', e)
            return False
            
    def check_exist_id(self, ncc_id) -> bool:
        logging.info('Checking ncc exist by id %s', ncc_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {NCC_TABLE} WHERE id = ?', (ncc_id,))
            data = self.cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking ncc exist %s', e)
            return False

    def __del__(self):
        logging.info('Closing database connection')
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    
