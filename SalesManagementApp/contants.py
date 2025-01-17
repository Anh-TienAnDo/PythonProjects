import os

CURRENT_WORKING_DIRECTORY = os.getcwd()
DATABASE_NAME = 'sales_management.db'
DATABASE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, 'database', DATABASE_NAME)
LOGGING_NAME = 'app.log'
LOGGING_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, LOGGING_NAME)
MAT_HANG_TABLE = 'MatHang'
BAN_HANG_TABLE = 'BanHang'
NHAP_HANG_TABLE = 'NhapHang'
KHACH_HANG_TABLE = 'KhachHang'
NCC_TABLE = 'NCC'
CHI_PHI_TABLE = 'ChiPhi'
DON_VI_TABLE = 'DonVi'

# ---- generate_id ----
MAT_HANG_ID_LENGTH = 6
MAT_HANG_ID_PREFIX = 'MH'

BAN_HANG_ID_LENGTH = 10
BAN_HANG_ID_PREFIX = 'BH'

NHAP_HANG_ID_LENGTH = 8
NHAP_HANG_ID_PREFIX = 'NH'

KHACH_HANG_ID_LENGTH = 6
KHACH_HANG_ID_PREFIX = 'KH'

NCC_ID_LENGTH = 6
NCC_ID_PREFIX = 'NCC'

CHI_PHI_ID_LENGTH = 10
CHI_PHI_ID_PREFIX = 'CP'

#  --- Title ---
TITLE_APP = 'Sales Management System'
TITLE_MAT_HANG = 'Quản lý mặt hàng'
TITLE_NHAP_HANG = 'Quản lý nhập hàng'
TITLE_BAN_HANG = 'Quản lý bán hàng'
TITLE_CHI_PHI = 'Quản lý chi phí'
TITLE_KHACH_HANG = 'Quản lý khách hàng'
TITLE_NCC = 'Quản lý nhà cung cấp'
TITLE_BAO_CAO = 'Báo cáo'

# template: 'Tên cột': 'Tên cột hiển thị'
MAT_HANG_COLUMN_NAMES = {
    'id': 'Mã hàng',
    'ten_hang': 'Tên hàng',
    'don_vi': 'Đơn vị',
    'so_luong': 'Số lượng',
    'gia_le': 'Giá lẻ',
    'gia_si': 'Giá sỉ',
    'ngay_tao': 'Ngày tạo',
    'is_active': 'Trạng thái'
}
#  sort_option: 'Tên cột': 'Tên cột hiển thị'
MAT_HANG_SORT_OPTIONS = {
    'Tên A-Z': 'ten_hang asc',
    'Tên Z-A': 'ten_hang desc',
    'Số lượng ít - nhiều': 'so_luong asc',
    'Số lượng nhiều - ít': 'so_luong desc',
    'Giá thấp - cao': 'gia_le asc',
    'Giá cao - thấp': 'gia_le desc',
    'Ngày tạo mới - cũ': 'ngay_tao asc',
    'Ngày tạo cũ - mới': 'ngay_tao desc'
}
  

# --- srceen ---
SCREEN_SIZE = "1920x1080"

# --- CSS ---
FAMILY_FONT = 'Arial'

# --- Color ---
BG_COLOR_LIGHT_BLUE = 'lightblue'
BG_COLOR_RED = 'red'
BG_COLOR_GREEN = 'green'
BG_COLOR_BLUE = 'blue'
BG_COLOR_YELLOW = 'yellow'
BG_COLOR_WHITE = 'white'
BG_COLOR_BLACK = 'black'
BG_COLOR_GRAY = 'gray'
BG_COLOR_LIGHT_GRAY = 'lightgray'
BG_COLOR_ORANGE = 'orange'

BG_COLOR_FRAME_MAIN = 'white'
BG_COLOR_FRAME_MAT_HANG = 'white'
BG_COLOR_FRAME_NHAP_HANG = 'white'
BG_COLOR_FRAME_BAN_HANG = 'white'
BG_COLOR_FRAME_CHI_PHI = 'white'
BG_COLOR_FRAME_KHACH_HANG = 'white'
BG_COLOR_FRAME_NCC = 'white'
BG_COLOR_FRAME_BAO_CAO = 'white'

BG_COLOR_FRAME_WHITE = 'white'

TEXT_COLOR = 'black'
TEXT_COLOR_RED = 'red'
TEXT_COLOR_GREEN = 'green'
TEXT_COLOR_BLUE = 'blue'
TEXT_COLOR_YELLOW = 'yellow'
TEXT_COLOR_WHITE = 'white'
TEXT_COLOR_LIGHT_BLUE = 'lightblue'
TEXT_COLOR_ORANGE = 'orange'

# --- button ---
WARP_LENGTH = 300
BUTTON_WARP_LENGTH = 300
BUTTON_BD = 3
BUTTON_HEIGHT = 3
BUTTON_WIDTH = 30
BUTTON_PADX = 5
BUTTON_PADY = 5
BUTTON_RELIEF = 'raised'
BUTTON_CURSOR = 'hand2'

#  --- Entry ---
ENTRY_BD = 3





