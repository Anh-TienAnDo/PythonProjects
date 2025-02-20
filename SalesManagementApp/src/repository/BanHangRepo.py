import sqlite3
from contants import BAN_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.BanHangEntity import BanHang
from src.utils.ConvertEntity import ConvertBanHang
from src.utils.Decorator import logger, timer

class BanHangRepo:
    @logger('BanHangRepo')
    @timer('BanHangRepo')
    def __init__(self):
        self.db_name = DATABASE_PATH
        self.convert_ban_hang = ConvertBanHang()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def get_all(self, sort_by: str, where: str, limit: str, offset:str) -> list[BanHang]:
        # logging.info('Getting all banhang')
        # logging.info('SELECT * FROM %s WHERE %s ORDER BY %s LIMIT %s OFFSET %s', BAN_HANG_TABLE, where, sort_by, limit, offset)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {BAN_HANG_TABLE} WHERE {where} ORDER BY {sort_by} LIMIT {limit} OFFSET {offset}')
            data = cursor.fetchall()
            ban_hang_list = self.convert_ban_hang.convert_to_entity_list(data)
            return ban_hang_list
        except Exception as e:
            logging.error('Error getting all %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
        
    def calculate_total(self, where: str):
        # logging.info('Calculating total ban hang %s', where)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT COUNT(*), SUM(so_luong), SUM(thanh_tien) FROM {BAN_HANG_TABLE} WHERE {where}')
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error('Error calculating total %s', e)
            return (0, 0, 0)
        finally:
            cursor.close()
            connection.close()
        
    def list(self) -> list[BanHang]:
        # logging.info('Getting all banhang')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT * FROM {BAN_HANG_TABLE}')
            data = cursor.fetchall()
            ban_hang_list = self.convert_ban_hang.convert_to_entity_list(data)
            return ban_hang_list
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
            cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien) FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY id_mat_hang ORDER BY {sort_by}')
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error('Error calculating report %s', e)
            return []
        finally:
            cursor.close()
            connection.close()

    def report_detail_mat_hang(self, sort_by: str, where: str) -> list:
        connection = self.get_connection()
        cursor = connection.cursor()
        # where: ngay_ban = '2021-09-01', id_mat_hang = 'MH0001'
        try:
            cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien), ngay_ban FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY ngay_ban ORDER BY {sort_by}')
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error('Error calculating detail mat hang %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
    
    def report_loi_nhuan(self, where: str) -> list:
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT sum(thanh_tien), ngay_ban FROM {BAN_HANG_TABLE} WHERE {where} GROUP BY ngay_ban')
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error('Error calculating loi nhuan %s', e)
            return []
        finally:
            cursor.close()
            connection.close()
            
    def get_by_id(self, ban_hang_id) -> BanHang:
        # logging.info('Getting banhang by id %s', ban_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {BAN_HANG_TABLE} WHERE id = ?', (ban_hang_id,))
            data = cursor.fetchone()
            return BanHang(*data) if data else None
        except Exception as e:
            logging.error('Error getting banhang by id %s', e)
            return None
        finally:
            cursor.close()
            connection.close()

    def create(self, ban_hang: BanHang) -> bool:
        # logging.info('Creating banhang %s', ban_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'''INSERT INTO {BAN_HANG_TABLE}
                                (id, id_mat_hang, ten_hang, don_vi, so_luong, gia_ban, khach_hang, thanh_tien, ghi_chu, ngay_ban) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ban_hang.to_tuple())
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating banhang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
    
    def create_many(self, ban_hang_list) -> bool:
        # logging.info('Creating multiple banhang records')
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            ban_hang_tuples = [ban_hang.to_tuple() for ban_hang in ban_hang_list]
            cursor.executemany(f'''INSERT INTO {BAN_HANG_TABLE}
                                    (id, id_mat_hang, ten_hang, don_vi, so_luong, gia_ban, khach_hang, thanh_tien, ghi_chu, ngay_ban) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ban_hang_tuples)
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error creating multiple banhang records %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def update(self, ban_hang_id, ban_hang: BanHang) -> bool:
        # logging.info('Updating banhang %s', ban_hang)
        connection = self.get_connection()
        cursor = connection.cursor()
        ten_hang = ban_hang.ten_hang
        don_vi = ban_hang.don_vi
        so_luong = ban_hang.so_luong
        gia_ban = ban_hang.gia_ban
        khach_hang = ban_hang.khach_hang
        thanh_tien = ban_hang.thanh_tien
        ghi_chu = ban_hang.ghi_chu
        try:
            cursor.execute(f'UPDATE {BAN_HANG_TABLE} SET ten_hang = ?, don_vi = ?, so_luong = ?, gia_ban = ?, khach_hang = ?, thanh_tien = ?, ghi_chu = ? WHERE id = ?', (
                ten_hang, don_vi, so_luong, gia_ban, khach_hang, thanh_tien, ghi_chu, ban_hang_id))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error updating banhang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    def delete(self, ban_hang_id) -> bool:
        # logging.info('Deleting banhang by id %s', ban_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'DELETE FROM {BAN_HANG_TABLE} WHERE id = ?', (ban_hang_id,))
            connection.commit()
            return True
        except Exception as e:
            logging.error('Error deleting banhang %s', e)
            return False
        finally:
            cursor.close()
            connection.close()
            
    def check_exist_id(self, ban_hang_id) -> bool:
        # logging.info('Checking banhang exist by id %s', ban_hang_id)
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                f'SELECT * FROM {BAN_HANG_TABLE} WHERE id = ?', (ban_hang_id,))
            data = cursor.fetchone()
            return True if data else False
        except Exception as e:
            logging.error('Error checking banhang exist %s', e)
            return False
        finally:
            cursor.close()
            connection.close()

    # def __del__(self):
    #     logging.info('Closing database connection to banhang')
    #     if cursor:
    #         cursor.close()
    #     if self.connection:
    #         self.connection.close()
        
    
