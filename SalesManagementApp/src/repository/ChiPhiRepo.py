import sqlite3
from contants import CHI_PHI_TABLE, DATABASE_PATH
import logging
from src.entity.ChiPhiEntity import ChiPhi


class ChiPhiRepo:
    def __init__(self):
        logging.info('---ChiPhiRepo initializing---')
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.info('Connected to database %s', DATABASE_PATH)

    def get_all(self, sort_by: str, where: str) -> list[ChiPhi]:
        logging.info('Getting all chi phi')
        try:
            self.cursor.execute(f'SELECT * FROM {CHI_PHI_TABLE} WHERE {where} ORDER BY {sort_by}')
            data = self.cursor.fetchall()
            chi_phi_list = [ChiPhi(*row) for row in data]
            return chi_phi_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all %s', e)
            return None
        
    def list(self) -> list[ChiPhi]:
        logging.info('Getting all chiphi')
        try:
            self.cursor.execute(f'SELECT * FROM {CHI_PHI_TABLE}')
            data = self.cursor.fetchall()
            chi_phi_list = [ChiPhi(*row) for row in data]
            return chi_phi_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all %s', e)

    def get_by_id(self, chi_phi_id) -> ChiPhi:
        logging.info('Getting chiphi by id %s', chi_phi_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {CHI_PHI_TABLE} WHERE id = ?', (chi_phi_id,))
            data = self.cursor.fetchone()
            return ChiPhi(*data) if data else None
        except sqlite3.IntegrityError as e:
            logging.error('Error getting chiphi by id %s', e)
            return None

    def create(self, chi_phi: ChiPhi) -> bool:
        logging.info('Creating chiphi %s', chi_phi)
        try:
            self.cursor.execute(f'''INSERT INTO {CHI_PHI_TABLE}
                                (id, ten_chi_phi, gia_chi_phi, ghi_chu, ngay_tao) 
                                VALUES (?, ?, ?, ?, ?)''', chi_phi.to_tuple())
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error creating chiphi %s', e)
            return False

    def update(self, chi_phi_id, chi_phi: ChiPhi) -> bool:
        logging.info('Updating chiphi %s', chi_phi)
        ten_chi_phi = chi_phi.ten_chi_phi
        gia_chi_phi = chi_phi.gia_chi_phi
        ghi_chu = chi_phi.ghi_chu
        try:
            self.cursor.execute(f'UPDATE {CHI_PHI_TABLE} SET ten_chi_phi = ?, gia_chi_phi = ?, ghi_chu = ? WHERE id = ?', (
                ten_chi_phi, gia_chi_phi, ghi_chu, chi_phi_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error updating chiphi %s', e)
            return False

    def delete(self, chi_phi_id) -> bool:
        logging.info('Deleting chiphi by id %s', chi_phi_id)
        try:
            self.cursor.execute(
                f'DELETE FROM {CHI_PHI_TABLE} WHERE id = ?', (chi_phi_id,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error deleting chiphi %s', e)
            return False
            
    def check_exist_id(self, chi_phi_id) -> bool:
        logging.info('Checking chiphi exist by id %s', chi_phi_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {CHI_PHI_TABLE} WHERE id = ?', (chi_phi_id,))
            data = self.cursor.fetchone()
            return True if data else False
        except sqlite3.IntegrityError as e:
            logging.error('Error checking chiphi exist %s', e)
            return False

    def __del__(self):
        logging.info('Closing database connection')
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    
