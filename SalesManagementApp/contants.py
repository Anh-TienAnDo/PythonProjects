import os

CURRENT_WORKING_DIRECTORY = os.getcwd()
DATABASE_NAME = 'sales_management.db'
DATABASE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, 'database', DATABASE_NAME)
LOGGING_NAME = 'app.log'
LOGGING_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, LOGGING_NAME)
WHOOSH_INDEX_DIR = 'indexdir'
WHOOSH_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, WHOOSH_INDEX_DIR)
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

KHACH_HANG_COLUMN_NAMES = {
    'id': 'Mã khách hàng',
    'ten_khach_hang': 'Tên khách hàng',
    'dien_thoai': 'Điện thoại',
    'email': 'Email',
    'dia_chi': 'Địa chỉ',
    'ghi_chu': 'Ghi chú',
    'ngay_tao': 'Ngày tạo',
    'is_active': 'Trạng thái'
}

NCC_COLUMN_NAMES = {
    'id': 'Mã nhà cung cấp',
    'ten_ncc': 'Tên nhà cung cấp',
    'dien_thoai': 'Điện thoại',
    'email': 'Email',
    'dia_chi': 'Địa chỉ',
    'ghi_chu': 'Ghi chú',
    'ngay_tao': 'Ngày tạo',
    'is_active': 'Trạng thái'
}

CHI_PHI_COLUMN_NAMES = {
    'id': 'Mã chi phí',
    'ten_chi_phi': 'Tên chi phí',
    'gia_chi_phi': 'Giá chi phí',
    'ghi_chu': 'Ghi chú',
    'ngay_tao': 'Ngày tạo'
}

NHAP_HANG_COLUMN_NAMES = {
    'id': 'Mã nhập hàng',
    'id_mat_hang': 'Mã hàng',
    'ten_hang': 'Tên hàng',
    'don_vi': 'Đơn vị',
    'so_luong': 'Số lượng',
    'gia_nhap': 'Giá nhập',
    'nha_cung_cap': 'Nhà cung cấp',
    'thanh_tien': 'Thành tiền',
    'ngay_nhap': 'Ngày nhập',
    'ghi_chu': 'Ghi chú'
}

BAN_HANG_COLUMN_NAMES = {
    'id': 'Mã bán hàng',
    'id_mat_hang': 'Mã hàng',
    'ten_hang': 'Tên hàng',
    'don_vi': 'Đơn vị',
    'so_luong': 'Số lượng',
    'gia_ban': 'Giá bán',
    'khach_hang': 'Khách hàng',
    'thanh_tien': 'Thành tiền',
    'ngay_ban': 'Ngày bán',
    'ghi_chu': 'Ghi chú'
}
#  sort_option: 'Tên cột': 'Tên cột hiển thị'
MAT_HANG_SORT_OPTIONS = {
    'Tên A-Z': 'ten_hang asc',
    'Tên Z-A': 'ten_hang desc',
    'Số lượng ít - nhiều': 'so_luong asc',
    'Số lượng nhiều - ít': 'so_luong desc',
    'Giá ít - nhiều': 'gia_le asc',
    'Giá nhiều - ít': 'gia_le desc',
    'Ngày tạo mới - cũ': 'ngay_tao desc',
    'Ngày tạo cũ - mới': 'ngay_tao asc'
}

KHACH_HANG_SORT_OPTIONS = {
    'Tên A-Z': 'ten_khach_hang asc',
    'Tên Z-A': 'ten_khach_hang desc',
    'Ngày tạo mới - cũ': 'ngay_tao desc',
    'Ngày tạo cũ - mới': 'ngay_tao asc'
}

NCC_SORT_OPTIONS = {
    'Tên A-Z': 'ten_ncc asc',
    'Tên Z-A': 'ten_ncc desc',
    'Ngày tạo mới - cũ': 'ngay_tao desc',
    'Ngày tạo cũ - mới': 'ngay_tao asc'
}

CHI_PHI_SORT_OPTIONS = {
    'Tên A-Z': 'ten_chi_phi asc',
    'Tên Z-A': 'ten_chi_phi desc',
    'Giá ít - nhiều': 'gia_chi_phi asc',
    'Giá nhiều - ít': 'gia_chi_phi desc',
    'Ngày tạo mới - cũ': 'ngay_tao desc',
    'Ngày tạo cũ - mới': 'ngay_tao asc'
}

NHAP_HANG_SORT_OPTIONS = {
    'Tên A-Z': 'ten_hang asc',
    'Tên Z-A': 'ten_hang desc',
    'Số lượng ít - nhiều': 'so_luong asc',
    'Số lượng nhiều - ít': 'so_luong desc',
    'Giá ít - nhiều': 'gia_nhap asc',
    'Giá nhiều - ít': 'gia_nhap desc',
    'Thành tiền ít - nhiều': 'thanh_tien asc',
    'Thành tiền nhiều - ít': 'thanh_tien desc',
    'Ngày nhập mới - cũ': 'ngay_nhap desc',
    'Ngày nhập cũ - mới': 'ngay_nhap asc'
}

REPORT_NHAP_HANG_SORT_OPTIONS = {
    'Ngày nhập mới - cũ': 'ngay_nhap desc',
    'Ngày nhập cũ - mới': 'ngay_nhap asc',
    'Số lần nhập ít - nhiều': 'count(id_mat_hang) asc',
    'Số lần nhập nhiều - ít': 'count(id_mat_hang) desc',
    'Tổng số lượng ít - nhiều': 'sum(so_luong) asc',
    'Tổng số lượng nhiều - ít': 'sum(so_luong) desc',
    'Tổng tiền ít - nhiều': 'sum(thanh_tien) asc',
    'Tổng tiền nhiều - ít': 'sum(thanh_tien) desc'
}

BAN_HANG_SORT_OPTIONS = {
    'Tên A-Z': 'ten_hang asc',
    'Tên Z-A': 'ten_hang desc',
    'Số lượng ít - nhiều': 'so_luong asc',
    'Số lượng nhiều - ít': 'so_luong desc',
    'Giá ít - nhiều': 'gia_ban asc',
    'Giá nhiều - ít': 'gia_ban desc',
    'Thành tiền ít - nhiều': 'thanh_tien asc',
    'Thành tiền nhiều - ít': 'thanh_tien desc',
    'Ngày bán mới - cũ': 'ngay_ban desc',
    'Ngày bán cũ - mới': 'ngay_ban asc'
}

REPORT_BAN_HANG_SORT_OPTIONS = {
    'Ngày bán mới - cũ': 'ngay_ban desc',
    'Ngày bán cũ - mới': 'ngay_ban asc',
    'Số lần bán ít - nhiều': 'count(id_mat_hang) asc',
    'Số lần bán nhiều - ít': 'count(id_mat_hang) desc',
    'Tổng số lượng ít - nhiều': 'sum(so_luong) asc',
    'Tổng số lượng nhiều - ít': 'sum(so_luong) desc',
    'Tổng tiền ít - nhiều': 'sum(thanh_tien) asc',
    'Tổng tiền nhiều - ít': 'sum(thanh_tien) desc'
}

TITLE_REPORT_NHAP_HANG = 'Báo cáo nhập hàng'
TITLE_REPORT_BAN_HANG = 'Báo cáo bán hàng'
COLUMNS_REPORT_NHAP_HANG = ['Mã hàng', 'Tên hàng', 'Số lần nhập', 'Tổng số lượng', 'Tổng tiền', 'Ngày nhập']
COLUMNS_REPORT_BAN_HANG = ['Mã hàng', 'Tên hàng', 'Số lần bán', 'Tổng số lượng', 'Tổng tiền', 'Ngày bán']
# --- srceen ---
SCREEN_SIZE = "1920x1080"

# --- CSS ---
FAMILY_FONT = 'Arial'
# FAMILY_FONT = 'Times New Roman'

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
BG_COLOR_BROWN = 'brown'

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
TEXT_COLOR_BROWN = 'brown'

# --- button ---
WARP_LENGTH = 200
BUTTON_WARP_LENGTH = 200
BUTTON_BD = 3
BUTTON_HEIGHT = 3
BUTTON_WIDTH = 30
BUTTON_PADX = 5
BUTTON_PADY = 5
BUTTON_RELIEF = 'raised'
BUTTON_CURSOR = 'hand2'

#  --- Entry ---
ENTRY_BD = 3

MONEY_UNIT = 'VNĐ'





