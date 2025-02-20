import sqlite3
from contants import CHI_PHI_TABLE, DATABASE_PATH
import logging
from src.entity.ChiPhiEntity import ChiPhi
from src.utils.ConvertEntity import ConvertChiPhi

class ChiPhiRepo:
    def __init__(self):
        logging.info('---ChiPhiRepo initializing---')
        self.db_name = DATABASE_PATH
        self.convert_chi_phi = ConvertChiPhi()
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all(self, sort_by: str, where: str, limit: str, offset: str) -> list[ChiPhi]:
        logging.info('Getting all chi phi')
        logging.info('SELECT * FROM %s WHERE %s ORDER BY %s LIMIT %s OFFSET %s', CHI_PHI_TABLE, where, sort_by, limit, offset)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {CHI_PHI_TABLE} WHERE {where} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}')
            data = cursor.fetchall()
            chi_phi_list = self.convert_chi_phi.convert_to_entity_list(data)
            return chi_phi_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def calculate_total(self, where: str):
        logging.info('Calculating total chi phi %s', where)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT COUNT(*), SUM(gia_chi_phi) FROM {CHI_PHI_TABLE} WHERE {where}')
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error('Error calculating total %s', e)
            return (0, 0)
        finally:
            cursor.close()
            connection.close()
        
    def list(self) -> list[ChiPhi]:
        logging.info('Getting all chiphi')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {CHI_PHI_TABLE}')
            data = cursor.fetchall()
            chi_phi_list = self.convert_chi_phi.convert_to_entity_list(data)
            return chi_phi_list
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
            cursor.execute(f'SELECT sum(gia_chi_phi), ngay_tao FROM {CHI_PHI_TABLE} WHERE {where} GROUP BY ngay_tao')
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error('Error getting report loi nhuan %s', e)
            return []
        finally:
            cursor.close()
            connection.close()

    def get_by_id(self, chi_phi_id) -> ChiPhi:
        logging.info('Getting chiphi by id %s', chi_phi_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {CHI_PHI_TABLE} WHERE id = ?', (chi_phi_id,))
            data = cursor.fetchone()
            return ChiPhi(*data) if data else None
        except Exception as e:
            logging.error('Error getting chiphi by id %s', e)
            return None
        finally:
            cursor.close()
            connection.close()

    def create(self, chi_phi: ChiPhi) -> bool:
        logging.info('Creating chiphi %s', chi_phi)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'''INSERT INTO {CHI_PHI_TABLE}
                                (id, ten_chi_phi, gia_chi_phi, ghi_chu, ngay_tao) 
                                VALUES (?, ?, ?, ?, ?)''', chi_phi.to_tuple())
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating chiphi %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
        
    def create_many(self, chi_phi_list) -> bool:
        logging.info('Creating chiphi %s', chi_phi_list)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.executemany(f'''INSERT INTO {CHI_PHI_TABLE}
                                (id, ten_chi_phi, gia_chi_phi, ghi_chu, ngay_tao) 
                                VALUES (?, ?, ?, ?, ?)''', [chi_phi.to_tuple() for chi_phi in chi_phi_list])
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating chiphi %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def update(self, chi_phi_id, chi_phi: ChiPhi) -> bool:
        logging.info('Updating chiphi %s', chi_phi)
        connection = self.get_connection()
        cursor = connection.cursor()
        ten_chi_phi = chi_phi.ten_chi_phi
        gia_chi_phi = chi_phi.gia_chi_phi
        ghi_chu = chi_phi.ghi_chu
        try:
            cursor.execute(f'UPDATE {CHI_PHI_TABLE} SET ten_chi_phi = ?, gia_chi_phi = ?, ghi_chu = ? WHERE id = ?', (
                ten_chi_phi, gia_chi_phi, ghi_chu, chi_phi_id))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating chiphi %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def delete(self, chi_phi_id) -> bool:
        logging.info('Deleting chiphi by id %s', chi_phi_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'DELETE FROM {CHI_PHI_TABLE} WHERE id = ?', (chi_phi_id,))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting chiphi %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
            
    def check_exist_id(self, chi_phi_id) -> bool:
        logging.info('Checking chiphi exist by id %s', chi_phi_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {CHI_PHI_TABLE} WHERE id = ?', (chi_phi_id,))
            data = cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking chiphi exist %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    # def __del__(self):
    #     logging.info('Closing database connection to chiphi')
    #     if cursor:
    #         cursor.close()
    #     if self.connection:
    #         self.connection.close()
        
    
