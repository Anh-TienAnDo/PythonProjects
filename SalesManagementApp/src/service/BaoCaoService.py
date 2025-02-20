import calendar
import logging
from datetime import datetime
from src.repository.BanHangRepo import BanHangRepo
from src.repository.NhapHangRepo import NhapHangRepo
from src.repository.ChiPhiRepo import ChiPhiRepo
from concurrent.futures import ThreadPoolExecutor

class BaoCaoService:
    def __init__(self):
        logging.info('---BaoCaoService initializing---')
        self.ban_hang_repo = BanHangRepo()
        self.nhap_hang_repo = NhapHangRepo()
        self.chi_phi_repo = ChiPhiRepo()
        
    def report_loi_nhuan(self, month: str, year: str) -> dict:
        try:
            now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            month = month.strip()
            year = year.strip()
            if month is None or month == '':
                month = str(now.month)
            if year is None or year == '':
                year = str(now.year)
            if len(month) == 1:
                month = f'0{month}'
            where_ban_hang = f"strftime('%m-%Y', ngay_ban) = '{month}-{year}'"
            where_nhap_hang = f"strftime('%m-%Y', ngay_nhap) = '{month}-{year}'"
            where_chi_phi = f"strftime('%m-%Y', ngay_tao) = '{month}-{year}'"
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.ban_hang_repo.report_loi_nhuan, where_ban_hang),
                            executor.submit(self.nhap_hang_repo.report_loi_nhuan, where_nhap_hang),
                            executor.submit(self.chi_phi_repo.report_loi_nhuan, where_chi_phi)]
            ban_hang, nhap_hang, chi_phi = [f.result() for f in futures]
            report = {}
            # Xác định số ngày trong tháng
            num_days = calendar.monthrange(int(year), int(month))[1]
            
            for d in [f'{year}-{month}-{day:02d}' for day in range(1, num_days + 1)]:
                report[d] = {
                    'ban_hang': 0,
                    'nhap_hang': 0,
                    'chi_phi': 0
                }
            for item in ban_hang:
                report[str(item[1])]['ban_hang'] = item[0] if item[0] is not None else 0
            for item in nhap_hang:
                report[str(item[1])]['nhap_hang'] = item[0] if item[0] is not None else 0
            for item in chi_phi:
                report[str(item[1])]['chi_phi'] = item[0] if item[0] is not None else 0

            return report
        except Exception as e:
            logging.error(f'Error: {e}')
            return {}
      
    def get_day_month_year(self) -> dict:
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        return {
            'day': str(now.day),
            'month': str(now.month),
            'year': str(now.year)
        }
        
    
        
