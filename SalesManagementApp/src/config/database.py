import sqlite3
from contants import *
import logging
import os

class Database:
    def __init__(self, db_name):
        logging.info('Connecting to database %s', db_name)
        if not os.path.exists(os.path.dirname(db_name)):
            os.makedirs(os.path.dirname(db_name))
        # database//sales_management.db
        self.db_name = db_name
        # Kết nối đến cơ sở dữ liệu SQLite (hoặc tạo cơ sở dữ liệu nếu chưa tồn tại) 
        self.connection = sqlite3.connect(self.db_name)
        # Tạo đối tượng con trỏ bằng phương thức cursor() 
        self.cursor = self.connection.cursor()
        
    def init_tables(self):
        logging.info('Initializing tables')
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {MAT_HANG_TABLE} (
            id VARCHAR(10) PRIMARY KEY,
            ten_hang VARCHAR(255) NOT NULL,
            don_vi VARCHAR(20),
            so_luong INTEGER DEFAULT 0,
            gia_le INTEGER DEFAULT 0,
            gia_si INTEGER DEFAULT 0,
            ngay_tao DATE DEFAULT CURRENT_DATE,
            is_active BOOLEAN DEFAULT 1
        )''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS mat_hang_idx_id ON {MAT_HANG_TABLE} (id)''')
        self.connection.commit()
        
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {BAN_HANG_TABLE} (
            id VARCHAR(14) PRIMARY KEY,
            id_mat_hang VARCHAR(10) NOT NULL,
            ten_hang VARCHAR(255) NOT NULL,
            don_vi VARCHAR(20),
            so_luong INTEGER NOT NULL,
            gia_ban INTEGER NOT NULL,
            khach_hang VARCHAR(10),
            thanh_tien INTEGER NOT NULL,
            ghi_chu VARCHAR(255),
            ngay_ban DATE DEFAULT CURRENT_DATE
        )''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS ban_hang_idx_id ON {BAN_HANG_TABLE} (id)''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS ban_hang_idx_id_mat_hang ON {BAN_HANG_TABLE} (id_mat_hang)''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS ban_hang_idx_year ON {BAN_HANG_TABLE} (strftime('%Y', ngay_ban))''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS ban_hang_idx_year_month ON {BAN_HANG_TABLE} (strftime('%Y-%m', ngay_ban))''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS ban_hang_idx_year_month_day ON {BAN_HANG_TABLE} (strftime('%Y-%m-%d', ngay_ban))''')
        self.connection.commit()

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {NHAP_HANG_TABLE} (
            id VARCHAR(12) PRIMARY KEY,
            id_mat_hang VARCHAR(10),
            ten_hang VARCHAR(255) NOT NULL,
            don_vi VARCHAR(20),
            so_luong INTEGER NOT NULL,
            gia_nhap INTEGER NOT NULL,
            nha_cung_cap VARCHAR(10),
            thanh_tien INTEGER NOT NULL,
            ghi_chu VARCHAR(255),
            ngay_nhap DATE DEFAULT CURRENT_DATE
        )''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS nhap_hang_idx_id ON {NHAP_HANG_TABLE} (id)''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS nhap_hang_idx_id_mat_hang ON {NHAP_HANG_TABLE} (id_mat_hang)''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS nhap_hang_idx_year ON {NHAP_HANG_TABLE} (strftime('%Y', ngay_nhap))''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS nhap_hang_idx_year_month ON {NHAP_HANG_TABLE} (strftime('%Y-%m', ngay_nhap))''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS nhap_hang_idx_year_month_day ON {NHAP_HANG_TABLE} (strftime('%Y-%m-%d', ngay_nhap))''')
        self.connection.commit()
        
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {CHI_PHI_TABLE} (
            id VARCHAR(14) PRIMARY KEY,
            ten_chi_phi VARCHAR(255) NOT NULL,
            gia_chi_phi INTEGER NOT NULL,
            ghi_chu VARCHAR(255),
            ngay_tao DATE DEFAULT CURRENT_DATE
        )''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS chi_phi_idx_id ON {CHI_PHI_TABLE} (id)''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS chi_phi_idx_year ON {CHI_PHI_TABLE} (strftime('%Y', ngay_tao))''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS chi_phi_idx_year_month ON {CHI_PHI_TABLE} (strftime('%Y-%m', ngay_tao))''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS chi_phi_idx_year_month_day ON {CHI_PHI_TABLE} (strftime('%Y-%m-%d', ngay_tao))''')
        self.connection.commit()
        
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {NCC_TABLE} (
            id VARCHAR(10) PRIMARY KEY,
            ten_ncc VARCHAR(255) NOT NULL,
            dien_thoai VARCHAR(12),
            email VARCHAR(255),
            dia_chi VARCHAR(255),
            ghi_chu VARCHAR(255),
            ngay_tao DATE DEFAULT CURRENT_DATE,
            is_active BOOLEAN DEFAULT 1
        )''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS ncc_idx_id ON {NCC_TABLE} (id)''')
        self.connection.commit()

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {KHACH_HANG_TABLE} (
            id VARCHAR(10) PRIMARY KEY,
            ten_khach_hang VARCHAR(255) NOT NULL,
            dien_thoai VARCHAR(12),
            email VARCHAR(255),
            dia_chi VARCHAR(255),
            ghi_chu VARCHAR(255),
            ngay_tao DATE DEFAULT CURRENT_DATE,
            is_active BOOLEAN DEFAULT 1
        )''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS kh_idx_id ON {KHACH_HANG_TABLE} (id)''')
        self.connection.commit()
        
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {DON_VI_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten VARCHAR(255) NOT NULL,
            ghi_chu VARCHAR(255),
            ngay_tao DATE DEFAULT CURRENT_DATE,
            is_active BOOLEAN DEFAULT 1
        )''')
        self.cursor.execute(f'''CREATE INDEX IF NOT EXISTS donvi_idx_id ON {DON_VI_TABLE} (id)''')
        self.connection.commit()
        
        self.connection.close()

    def __del__(self):
        self.connection.close()