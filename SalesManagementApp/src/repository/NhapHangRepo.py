import sqlite3
from contants import NHAP_HANG_TABLE, DATABASE_PATH
import logging
from src.entity.NhapHangEntity import NhapHang


class NhapHangRepo:
    def __init__(self):
        logging.info('---NhapHangRepo initializing---')
        self.db_name = DATABASE_PATH
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.info('Connected to database %s', DATABASE_PATH)

    def get_all(self, sort_by: str, where: str) -> list[NhapHang]:
        logging.info('Getting all nhaphang')
        try:
            self.cursor.execute(f'SELECT * FROM {NHAP_HANG_TABLE} WHERE {where} ORDER BY {sort_by}')
            data = self.cursor.fetchall()
            nhap_hang_list = [NhapHang(*row) for row in data]
            return nhap_hang_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all %s', e)
            return None
        
    def list(self) -> list[NhapHang]:
        logging.info('Getting all nhaphang')
        try:
            self.cursor.execute(f'SELECT * FROM {NHAP_HANG_TABLE}')
            data = self.cursor.fetchall()
            nhap_hang_list = [NhapHang(*row) for row in data]
            return nhap_hang_list
        except sqlite3.IntegrityError as e:
            logging.error('Error getting all %s', e)
            
    def report(self, sort_by: str, where: str) -> list:
        self.cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien) FROM {NHAP_HANG_TABLE} WHERE {where} GROUP BY id_mat_hang ORDER BY {sort_by}')
        data = self.cursor.fetchall()
        return data
    
    def report_detail_nhap_hang(self, sort_by: str, where: str) -> list:
        self.cursor.execute(f'SELECT id_mat_hang, ten_hang, count(id_mat_hang), sum(so_luong), sum(thanh_tien), ngay_nhap FROM {NHAP_HANG_TABLE} WHERE {where} GROUP BY ngay_nhap ORDER BY {sort_by}')
        data = self.cursor.fetchall()
        return data
    
    def report_loi_nhuan(self, where: str) -> list:
        self.cursor.execute(f'SELECT sum(thanh_tien), ngay_nhap FROM {NHAP_HANG_TABLE} WHERE {where} GROUP BY ngay_nhap')
        data = self.cursor.fetchall()
        return data

    def get_by_id(self, nhap_hang_id) -> NhapHang:
        logging.info('Getting nhaphang by id %s', nhap_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {NHAP_HANG_TABLE} WHERE id = ?', (nhap_hang_id,))
            data = self.cursor.fetchone()
            return NhapHang(*data) if data else None
        except sqlite3.IntegrityError as e:
            logging.error('Error getting nhaphang by id %s', e)
            return None

    def create(self, nhap_hang: NhapHang) -> bool:
        logging.info('Creating nhaphang %s', nhap_hang)
        try:
            self.cursor.execute(f'''INSERT INTO {NHAP_HANG_TABLE}
                                (id, id_mat_hang, ten_hang, don_vi, so_luong, gia_nhap, nha_cung_cap, thanh_tien, ghi_chu, ngay_nhap) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', nhap_hang.to_tuple())
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error creating nhaphang %s', e)
            return False

    def update(self, nhap_hang_id, nhap_hang: NhapHang) -> bool:
        logging.info('Updating nhaphang %s', nhap_hang)
        ten_hang = nhap_hang.ten_hang
        don_vi = nhap_hang.don_vi
        so_luong = nhap_hang.so_luong
        gia_nhap = nhap_hang.gia_nhap
        nha_cung_cap = nhap_hang.nha_cung_cap
        thanh_tien = nhap_hang.thanh_tien
        ghi_chu = nhap_hang.ghi_chu
        try:
            self.cursor.execute(f'UPDATE {NHAP_HANG_TABLE} SET ten_hang = ?, don_vi = ?, so_luong = ?, gia_nhap = ?, nha_cung_cap = ?, thanh_tien = ?, ghi_chu = ? WHERE id = ?', (
                ten_hang, don_vi, so_luong, gia_nhap, nha_cung_cap, thanh_tien, ghi_chu, nhap_hang_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error updating nhaphang %s', e)
            return False

    def delete(self, nhap_hang_id) -> bool:
        logging.info('Deleting nhaphang by id %s', nhap_hang_id)
        try:
            self.cursor.execute(
                f'DELETE FROM {NHAP_HANG_TABLE} WHERE id = ?', (nhap_hang_id,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            logging.error('Error deleting nhaphang %s', e)
            return False
            
    def check_exist_id(self, nhap_hang_id) -> bool:
        logging.info('Checking nhaphang exist by id %s', nhap_hang_id)
        try:
            self.cursor.execute(
                f'SELECT * FROM {NHAP_HANG_TABLE} WHERE id = ?', (nhap_hang_id,))
            data = self.cursor.fetchone()
            return True if data else False
        except sqlite3.IntegrityError as e:
            logging.error('Error checking nhaphang exist %s', e)
            return False

    def __del__(self):
        logging.info('Closing database connection')
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        
    
